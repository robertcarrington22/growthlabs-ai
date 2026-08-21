import { neon } from "@neondatabase/serverless";
const sql = neon(process.env.TEST_DB_URL);
const rows = await sql`SELECT * FROM leads ORDER BY id DESC LIMIT 3`;
console.log(JSON.stringify(rows, null, 1));
