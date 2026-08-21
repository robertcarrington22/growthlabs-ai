import { neon } from "@neondatabase/serverless";
const sql = neon(process.env.TEST_DB_URL);
await sql`DELETE FROM leads WHERE name = '' AND email = ''`;
const remaining = await sql`SELECT count(*)::int AS n FROM leads`;
console.log("test rows removed; leads remaining:", remaining[0].n);
