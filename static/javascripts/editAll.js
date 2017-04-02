var selectedModuleCount = 0;

//Show a module in the edit table
function showModuleInTable(selectedModuleCode, isModuleEdited) {
    selectedModuleCount++;
    var moduleRow = selectedModuleCode + "_row";
    document.getElementById(moduleRow).style.display = "table-row";
    document.getElementById(isModuleEdited).value = "True";
    if (selectedModuleCount > 0) {
        document.getElementById("edit-all-table-no-modules").style.display = "none";
    }
}

//Remove a module from the edit table
function removeModuleFromTable(moduleRow, isModuleEdited) {
    selectedModuleCount--;
    document.getElementById(moduleRow).style.display = "none";
    document.getElementById(isModuleEdited).value = "False";
    if (selectedModuleCount <= 0) {
        document.getElementById("edit-all-table-no-modules").style.display = "table-row";
    }
}

//Disable quota input when mounting is unchecked, enable quota input when checked
function toggleQuotaState(id) {
    var state = document.getElementById(id).disabled;
    document.getElementById(id).disabled = !state;
}

//Prevent user from typing '-', '.', or 'e' in quota input
function checkQuotaKeypress() {
    var e = window.event
    if(e.keyCode == 189 || e.keyCode == 190 || e.keyCode == 69) {
        e.preventDefault();
    }
}

//Add yellow highlight to mounting and quota if mounting is changed
function checkMountingChange(element, oldMounting, oldQuota, mountingID, quotaID) {
    var oldMounting = (oldMounting == 1);
    var newMounting = element.checked;

    if (oldMounting != newMounting) {
        addYellowHighlight(mountingID);
        addYellowHighlight(quotaID);
    } else {
        removeYellowHighlight(mountingID);
        removeYellowHighlight(quotaID);
        if (oldMounting == 1) {
            checkQuotaChange(document.getElementById(quotaID), oldQuota, quotaID)
        }
    }
}

//Add yellow highlight to quota if quota is changed
function checkQuotaChange(element, oldQuota, quotaID) {
    var newQuota = element.value;
    if (oldQuota == '?') oldQuota = '';
    if (oldQuota != newQuota) {
        addYellowHighlight(quotaID);
    } else {
        removeYellowHighlight(quotaID);
    }
}

function addYellowHighlight(id) {
    document.getElementById(id).parentElement.style.backgroundColor = "#fffdcc";
}

function removeYellowHighlight(id) {
    document.getElementById(id).parentElement.style.backgroundColor = "white";
}

//Reset the mounting and quota of a module to when page first load
function resetMountingAndQuota(sem1Mounting, sem2Mounting, sem1Quota, sem2Quota,
                               sem1MountingOption, sem2MountingOption,
                               sem1QuotaInput, sem2QuotaInput) {
    if (sem1Quota == '-' || sem1Quota == '?') sem1Quota = '';
    document.getElementById(sem1QuotaInput).value = sem1Quota;
    removeYellowHighlight(sem1QuotaInput);
    if (sem2Quota == '-' || sem2Quota == '?') sem2Quota = '';
    document.getElementById(sem2QuotaInput).value = sem2Quota;
    removeYellowHighlight(sem2QuotaInput);

    sem1Mounting = (sem1Mounting == 1);
    var sem1MountingNew = document.getElementById(sem1MountingOption).checked;
    if (sem1MountingNew != sem1Mounting) {
        toggleQuotaState(sem1QuotaInput);
    }
    document.getElementById(sem1MountingOption).checked = sem1Mounting;
    removeYellowHighlight(sem1MountingOption);

    sem2Mounting = (sem2Mounting == 1);
    var sem2MountingNew = document.getElementById(sem2MountingOption).checked;
    if (sem2MountingNew != sem2Mounting) {
        toggleQuotaState(sem2QuotaInput);
    }
    document.getElementById(sem2MountingOption).checked = sem2Mounting;
    removeYellowHighlight(sem2MountingOption);
}