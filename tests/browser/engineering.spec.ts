import {test,expect} from '@playwright/test';
import {readFile} from 'node:fs/promises';
test('engineering evidence changes checkpoint and downloads measured results',async({page})=>{
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('./');await page.getByRole('link',{name:'Engineering',exact:true}).click();
 await expect(page.getByRole('heading',{name:'Good data survives a bad day.'})).toBeVisible();
 await expect(page.getByTestId('return-total')).toHaveText('$75.00');
 await page.getByRole('button',{name:'Before correction'}).click();
 await expect(page.getByTestId('return-total')).toHaveText('$70.00');
 await page.getByRole('button',{name:'After correction'}).click();
 await expect(page.getByTestId('return-total')).toHaveText('$75.00');
 const pending=page.waitForEvent('download');await page.getByRole('button',{name:'Download evidence'}).click();const dl=await pending;
 const json=JSON.parse(await readFile((await dl.path())!,'utf8'));
 expect(json.evidence.final.reconciled).toBe(true);expect(json.benchmark.runs[1].rows).toBe(1000000);
 await page.screenshot({path:'test-results/engineering-light.png',fullPage:true});
 await page.getByRole('button',{name:'Switch to dark theme'}).click();
 await page.screenshot({path:'test-results/engineering-dark.png',fullPage:true});
 expect(errors).toEqual([]);
});
test('engineering mobile page remains readable and links back to the graph',async({page})=>{
 await page.setViewportSize({width:390,height:844});await page.goto('./?page=engineering');
 await expect(page.getByRole('heading',{name:'Good data survives a bad day.'})).toBeVisible();
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);
 await page.screenshot({path:'test-results/engineering-mobile.png',fullPage:true});
 await page.getByRole('link',{name:'Model explorer',exact:true}).click();
 await expect(page.getByRole('heading',{name:'A bank, connected.'})).toBeVisible();
});
