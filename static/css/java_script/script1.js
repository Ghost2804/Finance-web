// Loan EMI Calculator
function calculateEMI() {
    let loanAmount = document.getElementById("loanAmount").value;
    let interestRate = document.getElementById("interestRate").value / 100 / 12;
    let loanTenure = document.getElementById("loanTenure").value * 12;

    let emi = (loanAmount * interestRate * Math.pow(1 + interestRate, loanTenure)) / 
              (Math.pow(1 + interestRate, loanTenure) - 1);

    document.getElementById("emiResult").innerText = emi.toFixed(2);
}

// Investment Calculator (Compound Interest)
function calculateInvestment() {
    let investAmount = document.getElementById("investAmount").value;
    let investRate = document.getElementById("investRate").value / 100;
    let investYears = document.getElementById("investYears").value;

    let futureValue = investAmount * Math.pow(1 + investRate, investYears);
    document.getElementById("investResult").innerText = futureValue.toFixed(2);
}

// Budget Planner
function calculateBudget() {
    let income = document.getElementById("income").value;
    let expenses = document.getElementById("expenses").value;

    let savings = income - expenses;
    document.getElementById("budgetResult").innerText = savings;
}

// Retirement Savings Estimator
function calculateRetirement() {
    let currentAge = document.getElementById("currentAge").value;
    let retirementAge = document.getElementById("retirementAge").value;
    let monthlySavings = document.getElementById("monthlySavings").value;
    let retireRate = document.getElementById("retireRate").value / 100 / 12;

    let monthsLeft = (retirementAge - currentAge) * 12;
    let retirementSavings = monthlySavings * ((Math.pow(1 + retireRate, monthsLeft) - 1) / retireRate);

    document.getElementById("retireResult").innerText = retirementSavings.toFixed(2);
}
