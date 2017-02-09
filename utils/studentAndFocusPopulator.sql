--Students--
INSERT INTO student VALUES('D1000000A', 1);
INSERT INTO student VALUES('D2000000A', 2);
INSERT INTO student VALUES('D3000000A', 3);
INSERT INTO student VALUES('D4000000A', 4);
INSERT INTO student VALUES('D1000001A', 1);
INSERT INTO student VALUES('D2000001A', 2);
INSERT INTO student VALUES('D3000001A', 3);
INSERT INTO student VALUES('D4000001A', 4);
INSERT INTO student VALUES('D1000002A', 1);
INSERT INTO student VALUES('D2000002A', 2);
INSERT INTO student VALUES('D3000002A', 3);
INSERT INTO student VALUES('D4000002A', 4);

--Focus Areas--
INSERT INTO focusArea VALUES('Algorithms & Theory');
INSERT INTO focusArea VALUES('Artificial Intelligence');
INSERT INTO focusArea VALUES('Computer Graphics and Games');
INSERT INTO focusArea VALUES('Computer Security');
INSERT INTO focusArea VALUES('Database Systems');
INSERT INTO focusArea VALUES('Multimedia Information Retrieval');
INSERT INTO focusArea VALUES('Networking and Distributed Systems');
INSERT INTO focusArea VALUES('Parallel Computing');
INSERT INTO focusArea VALUES('Programming Languages');
INSERT INTO focusArea VALUES('Software Engineering');

--Takes Focus Areas--
INSERT INTO takesFocusArea VALUES('D1000000A', 'Artificial Intelligence', NULL);
INSERT INTO takesFocusArea VALUES('D2000000A', 'Artificial Intelligence', NULL);
INSERT INTO takesFocusArea VALUES('D3000000A', 'Artificial Intelligence', NULL);
INSERT INTO takesFocusArea VALUES('D4000000A', 'Artificial Intelligence', 'Computer Graphics and Games');
INSERT INTO takesFocusArea VALUES('D1000001A', 'Computer Graphics and Games', NULL);
INSERT INTO takesFocusArea VALUES('D2000001A', 'Computer Graphics and Games', NULL);
INSERT INTO takesFocusArea VALUES('D3000001A', 'Computer Graphics and Games', NULL);
INSERT INTO takesFocusArea VALUES('D4000001A', 'Computer Graphics and Games', 'Database Systems');
INSERT INTO takesFocusArea VALUES('D1000002A', 'Database Systems', NULL);
INSERT INTO takesFocusArea VALUES('D2000002A', 'Database Systems', NULL);
INSERT INTO takesFocusArea VALUES('D3000002A', 'Database Systems', NULL);
INSERT INTO takesFocusArea VALUES('D4000002A', 'Database Systems', 'Artificial Intelligence');
