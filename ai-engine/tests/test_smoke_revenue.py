"""End-to-end smoke test: revenue audit pipeline (sample data -> run_audit -> report)."""

import json

import pytest

from sample_data_generator import generate_sample_data
from main import run_audit


@pytest.fixture(scope="module")
def revenue_report(tmp_path_factory):
    """Run the full revenue audit once on generated sample data."""
    tmp = tmp_path_factory.mktemp("revenue_smoke")
    cust_path, txn_path = generate_sample_data(
        num_customers=120,
        num_transactions=3000,
        output_dir=str(tmp / "sample_data"),
    )
    report = run_audit(
        transactions_path=txn_path,
        customers_path=cust_path,
        output_path=str(tmp / "report.json"),
        client_name="Smoke Test Client",
        print_summary=False,
    )
    return report


def test_report_is_dict_with_metadata(revenue_report):
    assert isinstance(revenue_report, dict)
    assert revenue_report["report_metadata"]["client"] == "Smoke Test Client"


def test_executive_summary_present(revenue_report):
    exec_summary = revenue_report.get("executive_summary")
    assert isinstance(exec_summary, dict) and exec_summary
    assert "key_metrics" in exec_summary
    assert "finding_summary" in exec_summary
    assert exec_summary["key_metrics"]["total_revenue_analyzed"] > 0


def test_at_least_10_recommendations(revenue_report):
    findings = revenue_report.get("all_findings", [])
    assert len(findings) >= 10, f"Expected >=10 recommendations, got {len(findings)}"


def test_findings_are_quantified(revenue_report):
    findings = revenue_report.get("all_findings", [])
    assert findings, "all_findings is empty"
    for f in findings:
        assert "estimated_annual_impact_mid" in f, f"missing impact key in: {f.get('area')}"
        assert "confidence" in f, f"missing confidence in: {f.get('area')}"
        assert "effort" in f, f"missing effort in: {f.get('area')}"


def test_no_euro_symbol_anywhere(revenue_report):
    serialized = json.dumps(revenue_report, default=str, ensure_ascii=False)
    assert "€" not in serialized, "Euro symbol found in report — US market uses $"


def test_report_saved_to_disk_is_valid_json(revenue_report, tmp_path_factory):
    # run_audit already saved report.json in the module fixture's tmp dir
    tmp_dirs = [p for p in tmp_path_factory.getbasetemp().iterdir() if p.name.startswith("revenue_smoke")]
    report_files = [p / "report.json" for p in tmp_dirs if (p / "report.json").exists()]
    assert report_files, "report.json was not written"
    with open(report_files[0], encoding="utf-8") as f:
        on_disk = json.load(f)
    assert on_disk["report_metadata"]["client"] == "Smoke Test Client"
