import { chromium } from 'playwright';
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args:['--no-sandbox'] });
const p = await b.newPage({ deviceScaleFactor: 2 });
await p.setViewportSize({ width: 980, height: 1400 });
await p.goto('file:///home/user/Ashton-Hall-Africa-Tour/itinerary/itinerary.html', { waitUntil: 'networkidle' });
try { await p.evaluate(() => document.fonts.ready); } catch (e) {}
await p.waitForTimeout(1200);
const el = await p.$('.sheet');
await el.screenshot({ path: '/home/user/Ashton-Hall-Africa-Tour/itinerary/itinerary.png' });
await b.close();
console.log('rendered itinerary.png');
