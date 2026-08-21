import { neon } from "@neondatabase/serverless";
const sql = neon(process.env.TEST_DB_URL);
const rows = await sql`SELECT id, name, email, source, created_at FROM leads WHERE email = 'e2e-form-test@growthlabs.internal'`;
console.log("found:", JSON.stringify(rows));
await sql`DELETE FROM leads WHERE email = 'e2e-form-test@growthlabs.internal'`;
const remaining = await sql`SELECT count(*)::int AS n FROM leads`;
console.log("cleaned up; total leads remaining:", remaining[0].n);
