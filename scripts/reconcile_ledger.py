"""Reconcile a complete, single-currency period using independent balance snapshots."""
from decimal import Decimal

def reconcile(db, period):
    opening,closing=period['opening'],period['closing']
    if opening>=closing:raise AssertionError('Opening date must precede closing date')
    issues=[];ledger={};controls={}
    chart=[r[0] for r in db.execute('SELECT gl_account_id FROM gl_account ORDER BY gl_account_id').fetchall()]
    snapshots={}
    for date in (opening,closing):
        rows=dict(db.execute('SELECT gl_account_id,signed_balance FROM gl_balance_snapshot WHERE as_of_date=?',[date]).fetchall())
        if set(rows)!=set(chart):issues.append('Missing ledger snapshot at '+date)
        if sum(rows.values(),Decimal(0))!=0:issues.append('Unbalanced trial balance at '+date)
        snapshots[date]=rows
    for gl in chart:
        start=snapshots[opening].get(gl);end=snapshots[closing].get(gl)
        movement=db.execute("SELECT coalesce(sum(CASE WHEN l.direction='DEBIT' THEN l.amount ELSE -l.amount END),0) FROM journal_line l JOIN journal j USING(journal_id) WHERE l.gl_account_id=? AND j.status='POSTED' AND j.booked_on>? AND j.booked_on<=?",[gl,opening,closing]).fetchone()[0]
        if start is None or end is None:continue
        if start+movement!=end:issues.append('Ledger roll-forward mismatch: '+gl)
        ledger[gl]={'opening':str(start),'movement':str(movement),'closing':str(end)}
    accounts=db.execute('SELECT a.account_id,m.gl_account_id,p.kind FROM account a LEFT JOIN account_gl_mapping m USING(account_id) JOIN product_version v USING(product_version_id) JOIN product p USING(product_id)').fetchall()
    for aid,gl,kind in accounts:
        rows=dict(db.execute('SELECT as_of_date::VARCHAR,balance_amount FROM account_balance_snapshot WHERE account_id=? AND as_of_date IN (?,?)',[aid,opening,closing]).fetchall())
        if opening in rows and closing in rows:
            movement=db.execute("SELECT coalesce(sum(CASE WHEN direction='DEBIT' THEN amount ELSE -amount END),0) FROM account_entry WHERE account_id=? AND posted_on>? AND posted_on<=?",[aid,opening,closing]).fetchone()[0]
            if rows[opening]+movement*(-1 if kind=='DEPOSIT' else 1)!=rows[closing]:issues.append('Customer account roll-forward mismatch: '+aid)
    for date in (opening,closing):
        totals={}
        for aid,gl,kind in accounts:
            row=db.execute('SELECT balance_amount FROM account_balance_snapshot WHERE account_id=? AND as_of_date=?',[aid,date]).fetchone()
            if row is None:issues.append('Missing account snapshot: '+aid+' at '+date);continue
            if gl is None:issues.append('Missing account control: '+aid);continue
            totals[gl]=totals.get(gl,Decimal(0))+row[0]*(-1 if kind=='DEPOSIT' else 1)
        for gl,value in totals.items():
            if snapshots[date].get(gl)!=value:issues.append('Subledger control mismatch: '+gl+' at '+date)
        controls[date]={k:str(v) for k,v in sorted(totals.items())}
    if issues:raise AssertionError('; '.join(issues))
    return {'period':period,'ledger_accounts':ledger,'subledger_controls':controls,'trial_balance_difference':'0.00','scope':'All supplied CAD accounts and posted journals in this period; no external-feed completeness claim.'}
