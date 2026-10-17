import {test,expect} from '@playwright/test';
import {readFile} from 'node:fs/promises';
test('overview, domain drill-down, table inspector and relationship navigation',async({page})=>{
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));await page.goto('./');
 await expect(page.getByRole('heading',{name:'A bank, connected.'})).toBeVisible();await expect(page.locator('canvas').first()).toBeVisible();
 await page.screenshot({path:'test-results/overview.png',fullPage:true});
 await page.getByRole('button',{name:'Cards 3',exact:true}).click();
 await expect(page.getByTestId('view-summary')).toContainText('3 entities');
 await page.locator('.entity-sublist').getByRole('button',{name:'card',exact:true}).click();
 await expect(page.locator('.entity-intro h2')).toHaveText('Card');
 await page.getByRole('tab',{name:/Relationships/}).click();
 await page.locator('.relationship-card').filter({hasText:'replaces_card_id'}).click();
 await expect(page.getByText('This is a self-reference:',{exact:false})).toBeVisible();
 expect(errors).toEqual([]);
});
test('column search reveals a table outside the active domain',async({page})=>{
 await page.goto('./?domain=cards&view=tables');
 await page.getByRole('textbox',{name:'Search tables and columns'}).fill('minimum_due');
 await page.locator('.column-result').filter({hasText:'minimum_due'}).click();
 await expect(page.locator('.entity-intro h2')).toHaveText('Statement');
 await expect(page.locator('#column-minimum_due')).toHaveClass(/highlight-column/);
 await expect(page).toHaveURL(/entity=statement/);await expect(page).not.toHaveURL(/domain=cards/);
 await page.reload();await expect(page.locator('.entity-intro h2')).toHaveText('Statement');
});
test('both journeys, focus mode, reset, and history work',async({page})=>{
 await page.goto('./');
 await page.locator('.journey-link').filter({hasText:'Investigate a disputed purchase'}).click();
 await expect(page.getByTestId('view-summary')).toContainText('7 entities · 6 relationships');
 await page.locator('.journey-steps').getByRole('button',{name:/Card Transaction/}).click();
 await page.screenshot({path:'test-results/disputed-purchase.png',fullPage:true});
 await page.getByRole('button',{name:'Focus on relationships'}).click();await expect(page).toHaveURL(/focus=card_transaction/);
 await page.locator('.journey-link').filter({hasText:'Explain a monthly statement'}).click();
 await expect(page.getByTestId('view-summary')).toContainText('7 entities · 6 relationships');
 await page.getByRole('button',{name:'Reset',exact:true}).click();await expect(page.getByRole('heading',{name:'A bank, connected.'})).toBeVisible();
 await page.goBack();await expect(page.getByRole('heading',{name:'Explain a monthly statement'})).toBeVisible();
});
test('downloads contain model and dictionary data',async({page})=>{
 await page.goto('./');await page.getByText('Download',{exact:true}).click();
 const pending=page.waitForEvent('download');await page.getByRole('button',{name:/Model JSON/}).click();const dl=await pending;
 const data=JSON.parse(await readFile((await dl.path())!,'utf8'));expect(data.entities).toHaveLength(56);expect(data.relationships).toHaveLength(95);
 await page.getByText('Download',{exact:true}).click();const pending2=page.waitForEvent('download');await page.getByRole('button',{name:/Data dictionary/}).click();const dl2=await pending2;expect(await readFile((await dl2.path())!,'utf8')).toContain('minimum_due');
 await page.getByText('Download',{exact:true}).click();const pending3=page.waitForEvent('download');await page.getByRole('button',{name:/Current graph/}).click();const dl3=await pending3;expect((await readFile((await dl3.path())!)).subarray(1,4).toString()).toBe('PNG');
});
test('mobile navigation and inspector remain usable without horizontal overflow',async({page})=>{
 await page.setViewportSize({width:390,height:844});await page.goto('./');await page.getByRole('button',{name:'Browse model'}).click();
 await page.getByRole('textbox',{name:'Search tables and columns'}).fill('minimum_due');await page.locator('.column-result').filter({hasText:'minimum_due'}).click();
 await expect(page.locator('.inspector.mobile-open')).toBeVisible();await expect(page.locator('.entity-intro h2')).toHaveText('Statement');
 await page.screenshot({path:'test-results/mobile-inspector.png',fullPage:true});
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 await page.getByRole('button',{name:'Clear selection'}).click();await expect(page.locator('.inspector.mobile-open')).toHaveCount(0);
});
test('unknown URL state is explained and the graph still loads',async({page})=>{
 await page.goto('./?entity=missing');await expect(page.getByRole('status')).toContainText('unknown selection');await expect(page.locator('canvas').first()).toBeVisible();
});

test('expanded journeys and executable schema download',async({page})=>{
 for(const journey of ['onboard_a_customer','trace_a_deposit_payment','fund_a_term_loan','reconcile_to_the_ledger']){
  await page.goto('./?view=tables&journey='+journey);
  await expect(page.locator('.journey-strip')).toBeVisible();
  await expect(page.locator('.journey-steps button')).toHaveCount(journey==='trace_a_deposit_payment'?6:7);
 }
 await page.screenshot({path:'test-results/accounting-journey.png',fullPage:true});
 await page.getByText('Download',{exact:true}).click();
 const pending=page.waitForEvent('download');await page.getByRole('button',{name:/DuckDB schema/}).click();
 const file=await pending;const sql=await readFile((await file.path())!,'utf8');
 expect(sql).toContain('CREATE TABLE "journal"');expect(sql).toContain('CREATE TABLE "loan_contract"');
});

test('dusk theme persists, preserves navigation and exports its canvas',async({page})=>{
 await page.emulateMedia({colorScheme:'light'});await page.goto('./');
 await page.getByRole('button',{name:'Switch to dark theme'}).click();
 await expect(page.locator('html')).toHaveAttribute('data-theme','dark');
 await page.screenshot({path:'test-results/dark-overview.png',fullPage:true});
 await page.goto('./?view=tables&entity=gl_balance_snapshot');
 await expect(page.locator('.entity-intro h2')).toHaveText('Ledger Balance Snapshot');
 await expect(page.locator('html')).toHaveAttribute('data-theme','dark');
 await page.screenshot({path:'test-results/dark-inspector.png',fullPage:true});
 await page.getByText('Download',{exact:true}).click();const pending=page.waitForEvent('download');
 await page.getByRole('button',{name:/Current graph/}).click();const file=await pending;
 expect((await readFile((await file.path())!)).subarray(1,4).toString()).toBe('PNG');
 await page.setViewportSize({width:390,height:844});
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 await page.getByRole('button',{name:'Switch to light theme'}).click();await page.reload();
 await expect(page.locator('html')).toHaveAttribute('data-theme','light');
});
test('first visit honors the system dark preference',async({page})=>{
 await page.emulateMedia({colorScheme:'dark'});await page.goto('./');
 await expect(page.locator('html')).toHaveAttribute('data-theme','dark');
 await expect(page.getByRole('button',{name:'Switch to light theme'})).toBeVisible();
});
