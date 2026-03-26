const customCheckbox = document.getElementById("customDeliveryCheckbox");
const customFields = document.getElementById("customDeliveryFields");
const driverSelect = document.querySelector('select[name="driver_id"]');
const generateBtn = document.getElementById("generateBtn");

function toggleCustomFields() {
    customFields.style.display = customCheckbox.checked ? "block" : "none";
}

function toggleGenerateButton() {
    generateBtn.disabled = !driverSelect.value;
}

driverSelect.addEventListener("change", toggleGenerateButton);
toggleGenerateButton();

customCheckbox.addEventListener("change", toggleCustomFields);
toggleCustomFields();