#!/usr/bin/env python3
"""
GrowthLabs AI — Revenue Analysis Engine
Main entry point for running a full Discovery Audit.

Usage:
    python main.py --transactions data/transactions.csv --customers data/customers.csv --output report.json
    python main.py --sample                      # Run with generated sample data
"""

import argparse
import os
import sys
import json
from datetime import datetime

# Ensure we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data_ingestion import load_data, load_retail_data
from analysis.revenue_trends import analyze_revenue_trends
from analysis.customer_segments import analyze_customer_segments
from analysis.pricing import analyze_pricing
from report_generator import generate_report, save_report, print_report_summary
from sample_data_generator import generate_sample_data, generate_retail_sample_data
from nlp_summary import generate_full_summary
from pricing_proposal import calculate_retainer, format_retainer_summary
from analysis.industry_analysis import run_industry_analysis
from analysis.maturity_model import assess_maturity
from analysis.causal_loops import calculate_all_loops
from analysis.pattern_library import match_patterns, get_pattern_summary

# Inventory analysis modules (P8)
from analysis.inventory_classification import run_inventory_classification
from analysis.inventory_forecasting import run_inventory_forecasting
from analysis.inventory_policy import run_inventory_policy
from analysis.inventory_kpis import compute_all_kpis, format_kpi_scorecard
from analysis.inventory_report import run_inventory_audit


SAMPLE_DIR = "sample_data"
DEFAULT_OUTPUT = "revenue_audit_report.json"


def run_audit(
    transactions_path: str,
    customers_path: str,
    output_path: str = DEFAULT_OUTPUT,
    client_name: str = "Client Business",
    print_summary: bool = True,
) -> dict:
    """
    Run a full Discovery Audit pipeline.

    Args:
        transactions_path: Path to transactions CSV
        customers_path: Path to customers CSV (optional)
        output_path: Where to save the JSON report
        client_name: Client name for the report
        print_summary: Whether to print a summary to stdout

    Returns:
        The report dictionary
    """
    print("=" * 70)
    print("  GROWTHLABS AI — Revenue Discovery Audit Engine")
    print("=" * 70)

    # ── Step 1: Ingest ──
    print("\n📥 Step 1/4: Loading & validating data...")
    ingested = load_data(transactions_path, customers_path)

    if not ingested.is_valid:
        print(f"\n❌ Data validation failed:")
        for err in ingested.validation_errors:
            print(f"   • {err}")
        sys.exit(1)

    if ingested.warnings:
        print(f"\n⚠️  Data quality warnings:")
        for w in ingested.warnings:
            print(f"   • {w}")

    print(f"\n   ✅ Loaded {len(ingested.transactions)} transactions, {len(ingested.customers)} customers")

    # ── Step 2: Revenue Trends Analysis ──
    print("\n📈 Step 2/4: Analyzing revenue trends...")
    revenue_results = analyze_revenue_trends(ingested.transactions)
    if "error" in revenue_results:
        print(f"   ❌ {revenue_results['error']}")
    else:
        s = revenue_results["summary"]
        print(f"   ✅ Revenue: ${s['total_revenue']:,.2f} | {s['months_of_data']} months | AOV: ${s['avg_revenue_per_transaction']:,.2f}")

    # ── Step 3: Customer Analysis ──
    print("\n👥 Step 3/4: Analyzing customer segments...")
    customer_results = analyze_customer_segments(ingested.transactions, ingested.customers)
    if "error" in customer_results:
        print(f"   ❌ {customer_results['error']}")
    else:
        s = customer_results["summary"]
        print(f"   ✅ {s['total_customers']} customers | {s['active_customers']} active | {s['at_risk_customers']} at-risk")

    # ── Step 4: Pricing Analysis ──
    print("\n💰 Step 4/7: Analyzing pricing...")
    pricing_results = analyze_pricing(ingested.transactions, ingested.customers)
    if "error" in pricing_results:
        print(f"   ❌ {pricing_results['error']}")
    else:
        s = pricing_results["summary"]
        print(f"   ✅ AOV: ${s['overall_aov']:,.2f} | {s['total_services_offered']} services | {s['avg_services_per_customer']} avg per customer")

    # ── Step 5: Industry-Specific Analysis ──
    print("\n🏭 Step 5/7: Running industry-specific analysis...")
    industry_results = run_industry_analysis(ingested.transactions, ingested.customers)
    industry = industry_results.get("industry_detected", "generic")
    print(f"   ✅ Industry detected: {industry}")

    # ── Step 6: Maturity Model & Causal Loops ──
    print("\n📊 Step 6/7: Assessing maturity model and causal loops...")
    maturity_results = assess_maturity(ingested.transactions, ingested.customers)
    loops_results = calculate_all_loops(ingested.transactions, ingested.customers)
    print(f"   ✅ Maturity stage: {maturity_results['current_stage']} ({maturity_results['overall_score']}/100)")
    print(f"   ✅ Loop health: {loops_results['overall_loop_health']}/100 (weakest: {loops_results['weakest_loop']})")

    # ── Step 7: Pattern Library Matching ──
    temp_report = {
        "revenue_analysis": revenue_results,
        "customer_analysis": customer_results,
        "pricing_analysis": pricing_results,
        "industry_analysis": industry_results,
        "all_findings": [],
    }
    print("\n🔍 Step 7/7: Matching revenue gap patterns...")
    pattern_matches = match_patterns(temp_report)
    pattern_summary = get_pattern_summary(pattern_matches)
    print(f"   ✅ {pattern_summary['total']} patterns matched")

    # ── Generate Report ──
    print("\n📝 Generating report...")
    report = generate_report(
        revenue_analysis=revenue_results,
        customer_analysis=customer_results,
        pricing_analysis=pricing_results,
        ingestion_summary=ingested.summary(),
        client_name=client_name,
        industry_analysis=industry_results,
        maturity_assessment=maturity_results,
        causal_loops=loops_results,
        pattern_matches=pattern_matches,
        pattern_summary=pattern_summary,
    )

    save_report(report, output_path)

    if print_summary:
        print_report_summary(report)

    print(f"\n✅ Audit complete. Report saved to: {output_path}")
    return report


def _run_inventory_audit(args) -> dict:
    """Run the retail inventory audit pipeline from CLI args."""
    print("=" * 70)
    print("  GROWTHLABS AI — Retail Inventory Audit Engine")
    print("=" * 70)

    if not (args.sales and args.inventory_file and args.products):
        print("\n❌ Inventory audit requires --sales, --inventory-file and --products (or use --inventory-sample).")
        sys.exit(1)

    print("\n📥 Loading & validating retail data...")
    bundle = load_retail_data(args.sales, args.inventory_file, args.products, args.po)

    if bundle.validation_errors:
        print("\n❌ Data validation failed:")
        for err in bundle.validation_errors:
            print(f"   • {err}")
        sys.exit(1)

    if bundle.warnings:
        print("\n⚠️  Data quality warnings:")
        for w in bundle.warnings:
            print(f"   • {w}")

    print(f"\n   ✅ Loaded {len(bundle.sales)} sales rows, {len(bundle.products)} products, "
          f"{len(bundle.inventory_snapshots)} inventory records")

    print("\n📦 Running inventory analysis (classification → forecasting → policy → KPIs)...")
    po_df = bundle.purchase_orders if len(bundle.purchase_orders) > 0 else None
    result = run_inventory_audit(bundle.sales, bundle.inventory_snapshots, bundle.products, po_df)

    if "error" in result:
        print(f"\n❌ {result['error']}")
        sys.exit(1)

    report = {
        "report_metadata": {
            "title": f"GrowthLabs AI — Retail Inventory Audit: {args.client}",
            "client": args.client,
            "report_date": datetime.now().strftime("%Y-%m-%d"),
            "generated_by": "GrowthLabs AI Inventory Analysis Engine",
        },
        **result,
    }
    save_report(report, args.output)

    exec_summary = report.get("executive_summary", {})
    headline = exec_summary.get("headline")
    if headline:
        print(f"\n💡 {headline}")

    print(f"\n✅ Inventory audit complete. Report saved to: {args.output}")
    return report


def main():
    parser = argparse.ArgumentParser(
        description="GrowthLabs AI — Revenue Discovery Audit Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --sample
  python main.py --transactions data/transactions.csv --customers data/customers.csv
  python main.py --transactions data/transactions.csv --output my_report.json --client "Acme Corp"
  python main.py --inventory-sample                          # Retail inventory audit (sample data)
  python main.py --inventory --sales sales.csv --inventory inv.csv --products prods.csv
        """,
    )

    # Data source
    parser.add_argument("--transactions", "-t", help="Path to transactions CSV file")
    parser.add_argument("--customers", "-c", help="Path to customers CSV file")
    parser.add_argument("--sample", "-s", action="store_true", help="Generate and use sample data")

    # Inventory audit mode
    parser.add_argument("--inventory", action="store_true", help="Run inventory audit (requires --sales, --inventory, --products)")
    parser.add_argument("--inventory-sample", action="store_true", help="Run inventory audit with sample retail data")
    parser.add_argument("--sales", help="Path to retail sales CSV")
    parser.add_argument("--inventory-file", help="Path to inventory snapshots CSV")
    parser.add_argument("--products", help="Path to products master CSV")
    parser.add_argument("--po", help="Path to purchase orders CSV (optional)")

    # Output
    parser.add_argument("--output", "-o", default=DEFAULT_OUTPUT, help=f"Output report path (default: {DEFAULT_OUTPUT})")
    parser.add_argument("--client", "-n", default="Client Business", help="Client name for the report")
    parser.add_argument("--format", "-f", choices=["json", "pretty"], default="json",
                        help="Output format: 'json' (structured) or 'pretty' (human-readable markdown)")
    parser.add_argument("--quiet", "-q", action="store_true", help="Suppress printed summary")
    parser.add_argument("--num-customers", type=int, default=200, help="Sample data: number of customers")
    parser.add_argument("--num-transactions", type=int, default=5000, help="Sample data: number of transactions")
    parser.add_argument("--pricing", "-p", action="store_true",
                        help="Show retainer pricing proposal after the audit")

    args = parser.parse_args()

    # ── Inventory Audit Mode ──
    if args.inventory_sample:
        print("🔨 Generating synthetic retail inventory data...")
        sales_path, inv_path, prods_path = generate_retail_sample_data(output_dir="sample_retail_data")
        args.inventory = True
        args.sales = sales_path
        args.inventory_file = inv_path
        args.products = prods_path

    if args.inventory:
        _run_inventory_audit(args)
        return

    # ── Revenue Audit Mode (existing) ──
    if args.sample:
        print("🔨 Generating synthetic sample data...")
        cust_path, txn_path = generate_sample_data(
            num_customers=args.num_customers,
            num_transactions=args.num_transactions,
            output_dir=SAMPLE_DIR,
        )
    elif args.transactions:
        txn_path = args.transactions
        cust_path = args.customers
    else:
        parser.print_help()
        print("\n❌ Provide either --transactions or --sample to run an audit.")
        sys.exit(1)

    # Run the audit
    report = run_audit(
        transactions_path=txn_path,
        customers_path=cust_path,
        output_path=args.output,
        client_name=args.client,
        print_summary=not args.quiet,
    )

    # Print human-readable markdown summary if requested
    if args.format == "pretty":
        print("\n" + "=" * 70)
        print("  HUMAN-READABLE SUMMARY")
        print("=" * 70)
        summary = generate_full_summary(report, output_format="markdown")
        print(summary)

    # Print pricing proposal if requested
    if args.pricing:
        proposal = calculate_retainer(report)
        print("\n" + "=" * 70)
        print("  RETAINER PRICING PROPOSAL")
        print("=" * 70)
        print(format_retainer_summary(proposal))


if __name__ == "__main__":
    main()
