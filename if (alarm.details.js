if (alarm.details.createdValue !== undefined) {
    let valueStr = alarm.details.createdValue;
    // Extract numeric value using parseFloat and preserve the unit
    let value = parseFloat(valueStr);
    
    // Determine the unit from the original string (e.g., "%RH" or "°C")
    let unit = valueStr.replace(/[0-9.\s]/g, ''); // Removes numbers, periods, and spaces to get the unit
    
    // Check if value is a valid number
    if (!isNaN(value)) {
        // Reattach the unit and ensure one decimal place if value is an integer
        return Number.isInteger(value) ? value.toFixed(1) + " " + unit : value + " " + unit;
    } else {
        return valueStr; // Return original value with units if parsing fails
    }
} else {
    return "N/A";
}
