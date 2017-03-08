INSERT INTO module VALUES('MM1001', 'Dummy Modified Module 1', 'Quota of sem 1 is modified', 1);
INSERT INTO moduleMounted VALUES('MM1001', 'AY 16/17 Sem 1', 10);
INSERT INTO moduleMounted VALUES('MM1001', 'AY 16/17 Sem 2', 10);
INSERT INTO moduleMountTentative VALUES('MM1001', 'AY 17/18 Sem 1', 999);
INSERT INTO moduleMountTentative VALUES('MM1001', 'AY 17/18 Sem 2', 10);

INSERT INTO module VALUES('MM1002', 'Dummy Modified Module 2', 'Quota of sem 2 is modified', 2);
INSERT INTO moduleMounted VALUES('MM1002', 'AY 16/17 Sem 1', 20);
INSERT INTO moduleMounted VALUES('MM1002', 'AY 16/17 Sem 2', 20);
INSERT INTO moduleMountTentative VALUES('MM1002', 'AY 17/18 Sem 1', 20);
INSERT INTO moduleMountTentative VALUES('MM1002', 'AY 17/18 Sem 2', 888);

INSERT INTO module VALUES('MM1003', 'Dummy Modified Module 3', 'Quota of sem 1 has become specified', 3);
INSERT INTO moduleMounted VALUES('MM1003', 'AY 16/17 Sem 1', NULL);
INSERT INTO moduleMounted VALUES('MM1003', 'AY 16/17 Sem 2', NULL);
INSERT INTO moduleMountTentative VALUES('MM1003', 'AY 17/18 Sem 1', 777);
INSERT INTO moduleMountTentative VALUES('MM1003', 'AY 17/18 Sem 2', NULL);

INSERT INTO module VALUES('MM1004', 'Dummy Modified Module 4', 'Quota of sem 2 has become unspecified', 4);
INSERT INTO moduleMounted VALUES('MM1004', 'AY 16/17 Sem 1', 40);
INSERT INTO moduleMounted VALUES('MM1004', 'AY 16/17 Sem 2', 40);
INSERT INTO moduleMountTentative VALUES('MM1004', 'AY 17/18 Sem 1', 40);
INSERT INTO moduleMountTentative VALUES('MM1004', 'AY 17/18 Sem 2', NULL);

INSERT INTO module VALUES('MM1005', 'Dummy Modified Module 5', 'Quota of both sem 1 and sem 2 has been modified', 5);
INSERT INTO moduleMounted VALUES('MM1005', 'AY 16/17 Sem 1', 50);
INSERT INTO moduleMounted VALUES('MM1005', 'AY 16/17 Sem 2', 50);
INSERT INTO moduleMountTentative VALUES('MM1005', 'AY 17/18 Sem 1', NULL);
INSERT INTO moduleMountTentative VALUES('MM1005', 'AY 17/18 Sem 2', 666);

INSERT INTO module VALUES('MM1006', 'Dummy Modified Module 6', 'Unmounted from sem 1', 6);
INSERT INTO moduleMounted VALUES('MM1006', 'AY 16/17 Sem 1', 60);
INSERT INTO moduleMounted VALUES('MM1006', 'AY 16/17 Sem 2', 60);
INSERT INTO moduleMountTentative VALUES('MM1006', 'AY 17/18 Sem 2', 60);

INSERT INTO module VALUES('MM1007', 'Dummy Modified Module 7', 'Remounted in sem 2', 7);
INSERT INTO moduleMounted VALUES('MM1007', 'AY 16/17 Sem 1', 70);
INSERT INTO moduleMountTentative VALUES('MM1007', 'AY 17/18 Sem 1', 70);
INSERT INTO moduleMountTentative VALUES('MM1007', 'AY 17/18 Sem 2', 70);

INSERT INTO module VALUES('MM1008', 'Dummy Modified Module 8', 'Changed from mounted in sem 1 to sem 2', 8);
INSERT INTO moduleMounted VALUES('MM1008', 'AY 16/17 Sem 1', 80);
INSERT INTO moduleMountTentative VALUES('MM1008', 'AY 17/18 Sem 2', 80);

INSERT INTO module VALUES('MM1009', 'Dummy Modified Module 9', 'Name is modified', 9);
INSERT INTO moduleBackup VALUES('MM1009', 'Original Module Name', 'Name is modified', 9);

INSERT INTO module VALUES('MM1010', 'Dummy Modified Module 10', 'Description is modified', 10);
INSERT INTO moduleBackup VALUES('MM1010', 'Dummy Modified Module 10', 'Original Description', 10);

INSERT INTO module VALUES('MM1011', 'Dummy Modified Module 11', 'MC is modified', 0);
INSERT INTO moduleBackup VALUES('MM1011', 'Dummy Modified Module 11', 'MC is modified', 11);

INSERT INTO module VALUES('MM1012', 'Dummy Modified Module 12', 'Name and description are modified', 12);
INSERT INTO moduleBackup VALUES('MM1012', 'Original Module Name', 'Original Description', 12);

INSERT INTO module VALUES('MM1013', 'Dummy Modified Module 13', 'Mounting and name are modified', 1);
INSERT INTO moduleMounted VALUES('MM1013', 'AY 16/17 Sem 1', 130);
INSERT INTO moduleBackup VALUES('MM1013', 'Original Module Name', 'Mounting and name are modified', 1);

INSERT INTO module VALUES('MM1014', 'Dummy Modified Module 14', 'Quota and MC are modified', 2);
INSERT INTO moduleMounted VALUES('MM1014', 'AY 16/17 Sem 2', 140);
INSERT INTO moduleMountTentative VALUES('MM1014', 'AY 17/18 Sem 2', 555);
INSERT INTO moduleBackup VALUES('MM1014', 'Dummy Modified Module 14', 'Quota and MC are modified', 12);

INSERT INTO module VALUES('MM1015', 'Dummy Modified Module 8', 'Remounted in sem 1, but quota is not specified', 8);
INSERT INTO moduleMountTentative VALUES('MM1015', 'AY 17/18 Sem 2', NULL);
