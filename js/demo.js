// Demo Page Interactive JavaScript
// Advanced 3D Expense Tracker

let autoRotate = true;
let chartRotation = 0;

// ===== ADD EXPENSE SIMULATION =====
function addExpense() {
    const expenses = [
        { name: 'Coffee Shop', icon: 'fa-coffee', amount: -5.50 },
        { name: 'Gas Station', icon: 'fa-gas-pump', amount: -45.00 },
        { name: 'Movie Tickets', icon: 'fa-film', amount: -25.00 },
        { name: 'Grocery Store', icon: 'fa-shopping-cart', amount: -78.30 },
        { name: 'Uber Ride', icon: 'fa-car', amount: -12.50 },
    ];

    const random = expenses[Math.floor(Math.random() * expenses.length)];
    const list = document.getElementById('transaction-list');

    const tx = document.createElement('div');
    tx.className = 'demo-transaction';
    tx.style.opacity = '0';
    tx.style.transform = 'translateX(-20px)';
    tx.innerHTML = `
        <div class="tx-icon"><i class="fas ${random.icon}"></i></div>
        <div class="tx-details">
            <span class="tx-name">${random.name}</span>
            <span class="tx-date">Just now</span>
        </div>
        <span class="tx-amount expense">-$${Math.abs(random.amount).toFixed(2)}</span>
    `;

    list.insertBefore(tx, list.firstChild);

    // Animate in
    requestAnimationFrame(() => {
        tx.style.transition = 'all 0.4s ease-out';
        tx.style.opacity = '1';
        tx.style.transform = 'translateX(0)';
    });

    // Update total expense
    const expenseEl = document.getElementById('total-expense');
    const currentExpense = parseFloat(expenseEl.textContent.replace(/[$,]/g, ''));
    const newExpense = currentExpense + Math.abs(random.amount);
    animateValue(expenseEl, currentExpense, newExpense, 500, true);

    // Update balance
    updateBalance();

    // Remove old items if too many
    if (list.children.length > 6) {
        list.lastChild.remove();
    }
}

// ===== ADD INCOME SIMULATION =====
function addIncome() {
    const incomes = [
        { name: 'Freelance Project', icon: 'fa-laptop-code', amount: 500.00 },
        { name: 'Stock Dividend', icon: 'fa-chart-line', amount: 45.00 },
        { name: 'Refund', icon: 'fa-undo', amount: 30.00 },
        { name: 'Gift', icon: 'fa-gift', amount: 100.00 },
    ];

    const random = incomes[Math.floor(Math.random() * incomes.length)];
    const list = document.getElementById('transaction-list');

    const tx = document.createElement('div');
    tx.className = 'demo-transaction';
    tx.style.opacity = '0';
    tx.style.transform = 'translateX(-20px)';
    tx.innerHTML = `
        <div class="tx-icon"><i class="fas ${random.icon}"></i></div>
        <div class="tx-details">
            <span class="tx-name">${random.name}</span>
            <span class="tx-date">Just now</span>
        </div>
        <span class="tx-amount income">+$${random.amount.toFixed(2)}</span>
    `;

    list.insertBefore(tx, list.firstChild);

    requestAnimationFrame(() => {
        tx.style.transition = 'all 0.4s ease-out';
        tx.style.opacity = '1';
        tx.style.transform = 'translateX(0)';
    });

    const incomeEl = document.getElementById('total-income');
    const currentIncome = parseFloat(incomeEl.textContent.replace(/[$,]/g, ''));
    const newIncome = currentIncome + random.amount;
    animateValue(incomeEl, currentIncome, newIncome, 500, true);

    updateBalance();

    if (list.children.length > 6) {
        list.lastChild.remove();
    }
}

// ===== UPDATE BALANCE =====
function updateBalance() {
    const income = parseFloat(document.getElementById('total-income').textContent.replace(/[$,]/g, ''));
    const expense = parseFloat(document.getElementById('total-expense').textContent.replace(/[$,]/g, ''));
    const balanceEl = document.getElementById('net-balance');
    const savingsEl = document.getElementById('total-savings');

    const newBalance = income - expense;
    const currentBalance = parseFloat(balanceEl.textContent.replace(/[$,]/g, ''));
    animateValue(balanceEl, currentBalance, newBalance, 500, true);

    const newSavings = newBalance * 0.25;
    const currentSavings = parseFloat(savingsEl.textContent.replace(/[$,]/g, ''));
    animateValue(savingsEl, currentSavings, newSavings, 500, true);
}

// ===== ANIMATE VALUE =====
function animateValue(element, start, end, duration, isCurrency) {
    const range = end - start;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const easeProgress = 1 - Math.pow(1 - progress, 3);
        const current = start + range * easeProgress;

        if (isCurrency) {
            element.textContent = '$' + current.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        } else {
            element.textContent = Math.round(current).toLocaleString();
        }

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

// ===== DEMO 3D CHART (CANVAS 2D SIMULATION) =====
(function() {
    const canvas = document.getElementById('demo-3d-chart');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let width, height;

    function resize() {
        const rect = canvas.parentElement.getBoundingClientRect();
        canvas.width = rect.width;
        canvas.height = rect.height;
        width = canvas.width;
        height = canvas.height;
    }
    resize();
    window.addEventListener('resize', resize);

    // Data points
    const dataPoints = [
        { x: 0, income: 3000, expense: 2000, savings: 1000 },
        { x: 1, income: 3500, expense: 2200, savings: 1300 },
        { x: 2, income: 3200, expense: 1800, savings: 1400 },
        { x: 3, income: 4000, expense: 2500, savings: 1500 },
        { x: 4, income: 3800, expense: 2100, savings: 1700 },
        { x: 5, income: 4500, expense: 2300, savings: 2200 },
        { x: 6, income: 5200, expense: 2100, savings: 3100 },
    ];

    function drawChart() {
        ctx.clearRect(0, 0, width, height);

        const padding = 60;
        const chartWidth = width - padding * 2;
        const chartHeight = height - padding * 2;
        const maxValue = 6000;

        // Draw grid
        ctx.strokeStyle = 'rgba(0, 212, 255, 0.1)';
        ctx.lineWidth = 1;

        for (let i = 0; i <= 5; i++) {
            const y = padding + (chartHeight / 5) * i;
            ctx.beginPath();
            ctx.moveTo(padding, y);
            ctx.lineTo(width - padding, y);
            ctx.stroke();

            // Y-axis labels
            ctx.fillStyle = 'rgba(160, 160, 184, 0.6)';
            ctx.font = '10px Orbitron';
            ctx.textAlign = 'right';
            ctx.fillText('$' + (maxValue - (maxValue / 5) * i).toLocaleString(), padding - 10, y + 3);
        }

        // Draw 3D perspective lines
        const perspective = 0.3;
        const depth = 30;

        // Income line (cyan)
        draw3DLine(dataPoints, 'income', '#00d4ff', padding, chartWidth, chartHeight, maxValue, perspective, depth);

        // Expense line (red)
        draw3DLine(dataPoints, 'expense', '#ff4b4b', padding, chartWidth, chartHeight, maxValue, perspective, depth);

        // Savings line (green)
        draw3DLine(dataPoints, 'savings', '#00ff88', padding, chartWidth, chartHeight, maxValue, perspective, depth);

        // Draw data points with glow
        dataPoints.forEach((point, i) => {
            const x = padding + (chartWidth / (dataPoints.length - 1)) * i;

            ['income', 'expense', 'savings'].forEach((key, ki) => {
                const colors = ['#00d4ff', '#ff4b4b', '#00ff88'];
                const y = padding + chartHeight - (point[key] / maxValue) * chartHeight;

                // Glow
                const gradient = ctx.createRadialGradient(x, y, 0, x, y, 15);
                gradient.addColorStop(0, colors[ki] + '80');
                gradient.addColorStop(1, colors[ki] + '00');
                ctx.fillStyle = gradient;
                ctx.beginPath();
                ctx.arc(x, y, 15, 0, Math.PI * 2);
                ctx.fill();

                // Point
                ctx.fillStyle = colors[ki];
                ctx.beginPath();
                ctx.arc(x, y, 5, 0, Math.PI * 2);
                ctx.fill();

                // White center
                ctx.fillStyle = '#fff';
                ctx.beginPath();
                ctx.arc(x, y, 2, 0, Math.PI * 2);
                ctx.fill();
            });
        });

        // X-axis labels
        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'];
        dataPoints.forEach((point, i) => {
            const x = padding + (chartWidth / (dataPoints.length - 1)) * i;
            ctx.fillStyle = 'rgba(160, 160, 184, 0.6)';
            ctx.font = '10px Orbitron';
            ctx.textAlign = 'center';
            ctx.fillText(months[i], x, height - padding + 20);
        });
    }

    function draw3DLine(points, key, color, padding, chartWidth, chartHeight, maxValue, perspective, depth) {
        // Back line (3D depth)
        ctx.strokeStyle = color + '40';
        ctx.lineWidth = 2;
        ctx.beginPath();
        points.forEach((point, i) => {
            const x = padding + (chartWidth / (points.length - 1)) * i + depth * perspective;
            const y = padding + chartHeight - (point[key] / maxValue) * chartHeight - depth * perspective;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        });
        ctx.stroke();

        // Front line
        ctx.strokeStyle = color;
        ctx.lineWidth = 3;
        ctx.shadowColor = color;
        ctx.shadowBlur = 15;
        ctx.beginPath();
        points.forEach((point, i) => {
            const x = padding + (chartWidth / (points.length - 1)) * i;
            const y = padding + chartHeight - (point[key] / maxValue) * chartHeight;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        });
        ctx.stroke();
        ctx.shadowBlur = 0;

        // Fill area under line
        ctx.fillStyle = color + '15';
        ctx.beginPath();
        points.forEach((point, i) => {
            const x = padding + (chartWidth / (points.length - 1)) * i;
            const y = padding + chartHeight - (point[key] / maxValue) * chartHeight;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        });
        ctx.lineTo(padding + chartWidth, padding + chartHeight);
        ctx.lineTo(padding, padding + chartHeight);
        ctx.closePath();
        ctx.fill();
    }

    // Auto rotate animation
    function animate() {
        if (autoRotate) {
            chartRotation += 0.5;
        }
        drawChart();
        requestAnimationFrame(animate);
    }
    animate();
})();

// ===== CHART CONTROLS =====
function rotateChart(direction) {
    autoRotate = false;
    document.getElementById('rotate-icon').classList.remove('fa-spin');
    // In a real 3D implementation, this would rotate the camera
    console.log('Rotating chart:', direction);
}

function toggleAutoRotate() {
    autoRotate = !autoRotate;
    const icon = document.getElementById('rotate-icon');
    if (autoRotate) {
        icon.classList.add('fa-spin');
    } else {
        icon.classList.remove('fa-spin');
    }
}

// ===== DEMO SIDEBAR MENU INTERACTION =====
document.querySelectorAll('.demo-menu-item').forEach(item => {
    item.addEventListener('click', function() {
        document.querySelectorAll('.demo-menu-item').forEach(i => i.classList.remove('active'));
        this.classList.add('active');
    });
});
