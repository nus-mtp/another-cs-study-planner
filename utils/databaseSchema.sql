CREATE TABLE module (
code VARCHAR(10) PRIMARY KEY,
name VARCHAR(64),
description VARCHAR(4096),
mc INT,
status CHAR(14) CHECK(status = 'Active' or status = 'To Be Removed' or status = 'New') DEFAULT('Active')
);

CREATE TABLE moduleMounted(
moduleCode VARCHAR(10),
acadYearAndSem VARCHAR(14),
quota INT,
PRIMARY KEY (moduleCode, acadYearAndSem),
FOREIGN KEY (moduleCode) REFERENCES module(code)
);

CREATE TABLE moduleMountTentative (
moduleCode VARCHAR(10),
acadYearAndSem VARCHAR(14),
quota INT,
mountingPlanID INT DEFAULT(1),
PRIMARY KEY (acadYearAndSem, moduleCode, mountingPlanID),
FOREIGN KEY (moduleCode) REFERENCES module(code)
);

CREATE TABLE admin (
staffId VARCHAR(9) PRIMARY KEY,
salt VARCHAR(32),
password VARCHAR(256) NOT NULL,
isSuper BOOLEAN,
isActivated BOOLEAN
);
 
CREATE TABLE student (
nusnetId VARCHAR(9) PRIMARY KEY,
year INT
);

CREATE TABLE focusArea (
name VARCHAR(64) PRIMARY KEY
);

CREATE TABLE takesFocusArea (
nusnetId VARCHAR(9) PRIMARY KEY,
focusArea1 VARCHAR(64),
focusArea2 VARCHAR(64),
FOREIGN KEY (focusArea1) REFERENCES focusArea(name),
FOREIGN KEY (focusArea2) REFERENCES focusArea(name)
);
 
CREATE TABLE belongsToFocus (
moduleCode VARCHAR(10),
focusArea VARCHAR(64),
lastMounted DATE,
type VARCHAR(64),
PRIMARY KEY (moduleCode, focusArea),
FOREIGN KEY (moduleCode) REFERENCES module(code),
FOREIGN KEY (focusArea) REFERENCES focusArea(name)
);
 
CREATE TABLE precludes (
moduleCode VARCHAR(10),
precludedByModuleCode VARCHAR(10),
PRIMARY KEY (moduleCode, precludedByModuleCode),
FOREIGN KEY (moduleCode) REFERENCES module(code),
FOREIGN KEY (precludedByModuleCode) REFERENCES module(code),
CHECK (moduleCode != precludedByModuleCode)
);
 
CREATE TABLE prerequisite (
moduleCode VARCHAR(10),
prerequisiteModuleCode VARCHAR(10),
PRIMARY KEY (moduleCode, prerequisiteModuleCode),
FOREIGN KEY (moduleCode) REFERENCES module(code),
FOREIGN KEY (prerequisiteModuleCode) REFERENCES module(code),
index INT,
CHECK (moduleCode != prerequisiteModuleCode)
);
 
CREATE TABLE studentPlans (
studentId VARCHAR(9),
isTaken BOOLEAN,
moduleCode VARCHAR(10),
acadYearAndSem VARCHAR(20),
PRIMARY KEY (studentId, moduleCode, acadYearAndSem),
FOREIGN KEY (studentId) REFERENCES student(nusnetId)
);
 
CREATE TABLE starred(
moduleCode VARCHAR(10),
staffID VARCHAR(9),
PRIMARY KEY (moduleCode, staffID),
FOREIGN KEY (moduleCode) REFERENCES module(code),
FOREIGN KEY (staffID) REFERENCES admin(staffID)
);

CREATE TABLE moduleBackup (
code VARCHAR(10) PRIMARY KEY,
name VARCHAR(64),
description VARCHAR(4096),
mc INT
);
