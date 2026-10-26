"""Build the end-to-end fixture (M5): a small Node 20 app with the CSV-export task and the logout-after-reset bug.

Usage: python3 -I build_fixture.py <out dir>
Two commits: the working app, then (dated seven days earlier than now) the commit that introduces the bug.
"""
import os
import pathlib
import subprocess
import sys

out = pathlib.Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=False)
F = {
"package.json": '''{
  "name": "acme-app",
  "version": "1.0.0",
  "private": true,
  "engines": { "node": ">=20" },
  "scripts": { "test": "node --test" }
}
''',
"README.md": "# Acme app\n\nNode 20 service. Run the tests with `npm test`.\n\n- `src/reports.js`: the reports page. `renderReportsPage(rows, filter)` renders the rows the page shows after its filters.\n- `src/auth.js`: users, sessions, login and password reset.\n",
"src/reports.js": '''// The reports page: a table of report rows, narrowed by the filters the user picks.

const COLUMNS = ["id", "name", "region", "amount"];

// filter: { region?: string, minAmount?: number, text?: string }
function visibleRows(rows, filter = {}) {
  return rows.filter((r) => {
    if (filter.region && r.region !== filter.region) return false;
    if (filter.minAmount !== undefined && r.amount < filter.minAmount) return false;
    if (filter.text && !r.name.toLowerCase().includes(filter.text.toLowerCase())) return false;
    return true;
  });
}

function renderReportsPage(rows, filter = {}) {
  const shown = visibleRows(rows, filter);
  const head = "<tr>" + COLUMNS.map((c) => `<th>${c}</th>`).join("") + "</tr>";
  const body = shown.map((r) => "<tr>" + COLUMNS.map((c) => `<td>${r[c]}</td>`).join("") + "</tr>").join("");
  return `<table>${head}${body}</table><a href="/reports/export.csv">Export CSV</a>`;
}

// Export the rows the page shows as CSV. Not built yet.
function exportCsv(rows, filter = {}) {
  throw new Error("not implemented");
}

module.exports = { COLUMNS, visibleRows, renderReportsPage, exportCsv };
''',
"src/auth.js": '''// Users, sessions, login and password reset, kept in memory.
const crypto = require("node:crypto");

const users = new Map();     // email -> { email, passwordHash, sessionVersion }
const sessions = new Map();  // sessionId -> { email, version }
const resetTokens = new Map(); // token -> email

function hash(pw) {
  return crypto.createHash("sha256").update(pw).digest("hex");
}

function createUser(email, password) {
  users.set(email, { email, passwordHash: hash(password), sessionVersion: 1 });
}

function newSession(user) {
  const id = crypto.randomBytes(16).toString("hex");
  sessions.set(id, { email: user.email, version: user.sessionVersion });
  return id;
}

function login(email, password) {
  const user = users.get(email);
  if (!user || user.passwordHash !== hash(password)) return null;
  return newSession(user);
}

function currentUser(sessionId) {
  const s = sessions.get(sessionId);
  if (!s) return null;
  const user = users.get(s.email);
  if (!user || user.sessionVersion !== s.version) return null;
  return user.email;
}

function requestReset(email) {
  if (!users.has(email)) return null;
  const token = crypto.randomBytes(16).toString("hex");
  resetTokens.set(token, email);
  return token;
}

// Set a new password, end every older session, and sign the user in.
function resetPassword(token, newPassword) {
  const email = resetTokens.get(token);
  if (!email) return null;
  resetTokens.delete(token);
  const user = users.get(email);
  user.passwordHash = hash(newPassword);
  user.sessionVersion += 1;
  return newSession(user);
}

function _reset() {
  users.clear(); sessions.clear(); resetTokens.clear();
}

module.exports = { createUser, login, currentUser, requestReset, resetPassword, _reset };
''',
"test/reports.test.js": '''const test = require("node:test");
const assert = require("node:assert");
const { visibleRows, renderReportsPage } = require("../src/reports");

const rows = [
  { id: 1, name: "Alpha", region: "EU", amount: 10 },
  { id: 2, name: "Beta", region: "US", amount: 50 },
];

test("filters by region", () => {
  assert.deepStrictEqual(visibleRows(rows, { region: "US" }).map((r) => r.id), [2]);
});

test("page renders the visible rows", () => {
  const html = renderReportsPage(rows, { minAmount: 20 });
  assert.ok(html.includes("Beta"));
  assert.ok(!html.includes("Alpha"));
});
''',
"test/auth.test.js": '''const test = require("node:test");
const assert = require("node:assert");
const auth = require("../src/auth");

test("login with the right password", () => {
  auth._reset();
  auth.createUser("a@example.com", "old-pass");
  assert.ok(auth.currentUser(auth.login("a@example.com", "old-pass")));
});

test("login with a wrong password fails", () => {
  auth._reset();
  auth.createUser("a@example.com", "old-pass");
  assert.strictEqual(auth.login("a@example.com", "nope"), null);
});
''',
}
for rel, text in F.items():
    p = out / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)


def git(*a, env=None):
    subprocess.run(["git", "-C", str(out), *a], check=True, capture_output=True, env=env)


env = dict(os.environ, GIT_AUTHOR_NAME="dev", GIT_AUTHOR_EMAIL="dev@example.com", GIT_COMMITTER_NAME="dev", GIT_COMMITTER_EMAIL="dev@example.com")
git("init", "-q", "-b", "main")
# Commit 1: the working app, where the new session is issued after the version bump.
good = F["src/auth.js"]
(out / "src/auth.js").write_text(good)
e1 = dict(env, GIT_AUTHOR_DATE="2026-10-01T10:00:00", GIT_COMMITTER_DATE="2026-10-01T10:00:00")
git("add", "-A", env=e1)
git("commit", "-q", "-m", "Reports page and auth", env=e1)
# Commit 2, seven days before the run: issue the session before the version bump. The bug.
bad = good.replace("  user.sessionVersion += 1;\n  return newSession(user);\n",
                   "  const sessionId = newSession(user);\n  user.sessionVersion += 1; // end older sessions\n  return sessionId;\n")
assert bad != good
(out / "src/auth.js").write_text(bad)
e2 = dict(env, GIT_AUTHOR_DATE="2026-10-18T15:00:00", GIT_COMMITTER_DATE="2026-10-18T15:00:00")
git("add", "-A", env=e2)
git("commit", "-q", "-m", "Tidy password reset", env=e2)
print("ok", out)
