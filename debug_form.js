const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();
    
    // Capturar logs do console
    const logs = [];
    page.on('console', msg => {
        logs.push(`${msg.type()}: ${msg.text()}`);
    });
    
    await page.goto('http://localhost:8000/servicos/');
    await page.waitForTimeout(3000);
    
    // Clicar no primeiro botão de serviço
    await page.evaluate(() => {
        const serviceButtons = document.querySelectorAll('.service-card .btn-primary');
        if (serviceButtons.length > 0) {
            serviceButtons[0].click();
        }
    });
    
    await page.waitForTimeout(3000);
    
    // Verificar se os campos existem
    const cardNumberField = await page.$('#form-checkout__cardNumber input');
    const expirationField = await page.$('#form-checkout__expirationDate input');
    const securityCodeField = await page.$('#form-checkout__securityCode input');
    
    console.log('=== VERIFICAÇÃO DOS CAMPOS ===')
    console.log('Campo Número do Cartão encontrado:', !!cardNumberField);
    console.log('Campo Vencimento encontrado:', !!expirationField);
    console.log('Campo CVV encontrado:', !!securityCodeField);
    
    if (cardNumberField) {
        const fieldInfo = await page.evaluate(el => {
            const styles = window.getComputedStyle(el);
            return {
                disabled: el.disabled,
                readOnly: el.readOnly,
                pointerEvents: styles.pointerEvents,
                display: styles.display,
                visibility: styles.visibility,
                opacity: styles.opacity,
                zIndex: styles.zIndex,
                position: styles.position
            };
        }, cardNumberField);
        
        console.log('\n=== PROPRIEDADES DO CAMPO NÚMERO ===')
        console.log('Desabilitado:', fieldInfo.disabled);
        console.log('Somente leitura:', fieldInfo.readOnly);
        console.log('Pointer events:', fieldInfo.pointerEvents);
        console.log('Display:', fieldInfo.display);
        console.log('Visibility:', fieldInfo.visibility);
        console.log('Opacity:', fieldInfo.opacity);
        console.log('Z-index:', fieldInfo.zIndex);
        console.log('Position:', fieldInfo.position);
    }
    
    // Verificar se o SDK do Mercado Pago foi carregado
    const mpStatus = await page.evaluate(() => {
        return {
            mpExists: typeof MercadoPago !== 'undefined',
            windowMp: typeof window.mp !== 'undefined',
            cardForm: typeof window.cardForm !== 'undefined'
        };
    });
    
    console.log('\n=== STATUS DO MERCADO PAGO ===')
    console.log('MercadoPago SDK carregado:', mpStatus.mpExists);
    console.log('window.mp inicializado:', mpStatus.windowMp);
    console.log('cardForm inicializado:', mpStatus.cardForm);
    
    console.log('\n=== LOGS DO CONSOLE ===')
    logs.forEach(log => console.log(log));
    
    await browser.close();
})().catch(console.error);