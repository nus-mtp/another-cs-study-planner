UPDATE moduleMountTentative SET quota=250 WHERE moduleCode='CS2103' AND acadyearAndSem='AY 17/18 Sem 1';

UPDATE moduleMountTentative SET quota=800 WHERE moduleCode='CS2106' AND acadyearAndSem='AY 17/18 Sem 2';

UPDATE moduleMountTentative SET quota=40 WHERE moduleCode='CS3284' AND acadyearAndSem='AY 17/18 Sem 1';

UPDATE moduleMountTentative SET quota=NULL WHERE moduleCode='CS1010E' AND acadyearAndSem='AY 17/18 Sem 2';

UPDATE moduleMountTentative SET quota=NULL WHERE moduleCode='CS2102' AND acadyearAndSem='AY 17/18 Sem 1';
UPDATE moduleMountTentative SET quota=500 WHERE moduleCode='CS2102' AND acadyearAndSem='AY 17/18 Sem 2';

DELETE FROM moduleMountTentative WHERE moduleCode='CS2107' AND acadyearAndSem='AY 17/18 Sem 1';

INSERT INTO moduleMountTentative VALUES('CS4243', 'AY 17/18 Sem 2', 100);

DELETE FROM moduleMountTentative WHERE moduleCode='CS2107' AND acadyearAndSem='AY 17/18 Sem 1';

DELETE FROM moduleMountTentative WHERE moduleCode='CS2104' AND acadyearAndSem='AY 17/18 Sem 1';
INSERT INTO moduleMountTentative VALUES('CS2104', 'AY 17/18 Sem 2', 120);

INSERT INTO moduleBackup VALUES('CP2201', 'Journey of the Entrepreneur', 'Innovators practice the art of persuading people to accept changes in how they live and work, leisure and social interaction. This module&#39;s object is to introduce students to digital innovation, and to encourage them to embark on a personal journey of creativity and challenge. Inspirational innovators will be invited to present topics related to digital innovation, such as successful innovative projects of start-up teams and advanced development teams, innovative approaches such as Design Thinking, and opportunities for innovation, the vibrant intersection of energising technology trends and new markets. This module will be graded as Completed Satisfactory or Completed Unsatisfactory (CS/CU).', 2);

INSERT INTO moduleBackup VALUES('CS2010', 'Data Structures and Algorithms II', 'This module is the third part of a three-part series on introductory programming and problem solving by computing. It continues the introduction in CS1010 and CS1020, and emphasises object-oriented programming with application to complex data structures. Topics covered include trees, binary search trees, order property, prefix/infix/postfix expressions, heaps, priority queues, graphs and their algorithmic design, recursive algorithms, problem formulation and problem solving with applications of complex data structures, data structure design principles and implementation strategies, and algorithm analysis.', 4);

INSERT INTO moduleBackup VALUES('CS3103', 'Computer Networks Practice', 'This module aims to provide an opportunity for the students to learn commonly-used network protocols in greater technical depth with their implementation details than a basic networking course. Students will perform hands-on experiments in configuring and interconnecting LANs using networking devices/technologies (e.g., routers, switches, SDN switches, and hubs), networking protocols (e.g., DHCP, DNS, RIP, OSPF, ICMP, TCP, UDP, wireless LAN, VLAN protocols, SIP, SSL, IPSec-VPN) and networking tools (e.g, tcpdump, netstat, ping, traceroute). Students will learn higher-layer network protocols and develop network applications (client/server, P2P) via socket programming.', 2);

UPDATE moduleMountTentative SET quota=200 WHERE moduleCode='CG1001' AND acadyearAndSem='AY 17/18 Sem 1';
INSERT INTO moduleBackup VALUES('CG1001', 'Introduction to Computer Engineering', 'This module aims to provide an overview of Computer Engineering to the freshmen students. The module introduces the sub-areas, the issues, the impacts, and the challenges of Computer Engineering in transforming the world. The module demonstrates Computer Engineering as a multi-disciplinary field that transcends the traditional boundary of Computer Science and Electrical Engineering. It also gives the students an idea of the possible areas of specializations in their senior years of study.', 3);

INSERT INTO moduleMountTentative VALUES('CS1231', 'AY 17/18 Sem 2', 300);
INSERT INTO moduleBackup VALUES('CS1231', 'Discrete Structures', 'This module introduces mathematical tools required in the study of computer science. Topics include: (i) Logic and proof techniques: propositions, conditionals, quantifications. (ii) Relations and Functions: Equivalence relations and partitions. Partially ordered sets. Well-Ordering Principle. Function equality. Boolean/identity/inverse functions. Bijection. (iii) Mathematical formulation of data models (linear model, trees and graphs). (iv) Counting and Combinatoric: Pigeonhole Principle. Inclusion-Exclusion Principle. Number of relations on a set, number of injections from one finite set to another, Diagonalisation proof: An infinite countable set has an uncountable power set; Algorithmic proof: An infinite set has a countably infinite subset.', 4);
