PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE user (
	id INTEGER NOT NULL, 
	name VARCHAR(50) NOT NULL, 
	email VARCHAR(100) NOT NULL, 
	image_file VARCHAR(20) NOT NULL, 
	password VARCHAR(50) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (email)
);
INSERT INTO user VALUES(1,'user','user@email.com','9e62977666812a8e.jpg','$2b$12$DAfTzSsL52ASalRs3Q6JeudV/AO.sCOmNCXyIKw3a/kgAz4fu7huu');
INSERT INTO user VALUES(2,'User2','user2@email.com','default_profile.png','$2b$12$0KEYwlzHznwhGSYQMiU/m.f4CiBrSbIX4PauBpurWI9disbuDEiYG');
INSERT INTO user VALUES(3,'user3','user3@email.com','default_profile.png','$2b$12$rpYmPShuST2idniERdZFneAx3mWlYtCowSFsSmI0G1SSn4gP/gnD6');
INSERT INTO user VALUES(4,'Person 4','user4@email.com','default_profile.png','$2b$12$mcfoXV67GMFWx7SLG7G0jOjG/ei8zvli9KdXvfluYJjiX9Qu1u3E6');
INSERT INTO user VALUES(5,'user5','user5@email.com','default_profile.png','$2b$12$AdeGiapemV95fsMJvl6qKOFLyOqNCyFNQk0CCLm4hTiBOLduNEhga');
INSERT INTO user VALUES(6,'example','eg@email.com','default_profile.png','$2b$12$5OqdzT5jvDgOTIgqHVw89.I7oi0wHH.QGmSC63s7Z2LOebM1ZI69.');
CREATE TABLE type (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE project (
	id INTEGER NOT NULL, 
	name VARCHAR(250) NOT NULL, 
	"desc" VARCHAR(1000) NOT NULL, 
	date_created DATETIME NOT NULL, 
	creator_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(creator_id) REFERENCES user (id)
);
INSERT INTO project VALUES(1,'Module','Description','2023-08-08 09:32:41.039860',1);
INSERT INTO project VALUES(2,'MOdule 2','Desc','2023-08-09 14:04:47.770068',1);
INSERT INTO project VALUES(3,'Module 3','Desc','2023-08-10 16:28:54.459097',1);
INSERT INTO project VALUES(4,'Module','123','2023-08-14 10:33:39.719348',1);
INSERT INTO project VALUES(5,'Module 4','','2023-08-14 11:04:25.905313',1);
INSERT INTO project VALUES(6,'Example Module','Example Description','2023-08-17 13:24:10.588423',1);
INSERT INTO project VALUES(7,'Example Module','Example Description','2023-08-17 14:09:55.321604',1);
INSERT INTO project VALUES(8,'Example module','example desc','2023-08-18 13:14:46.636363',1);
INSERT INTO project VALUES(9,'Access test','','2023-08-23 12:42:23.383941',4);
INSERT INTO project VALUES(10,'s','','2023-08-29 11:52:05.754572',1);
INSERT INTO project VALUES(11,'Also viewable','','2023-08-31 17:12:45.910873',3);
INSERT INTO project VALUES(12,'Viewable','','2023-08-31 17:13:19.641042',3);
INSERT INTO project VALUES(13,'Not viewable','','2023-08-31 17:14:16.326195',3);
INSERT INTO project VALUES(14,'TEST','','2023-09-01 15:20:05.840373',5);
INSERT INTO project VALUES(15,'Project','','2023-09-04 11:48:16.011269',1);
INSERT INTO project VALUES(16,'Example module','Example desc','2023-09-05 14:06:49.011856',1);
INSERT INTO project VALUES(17,'Example Module','Description of Example module','2023-09-07 11:19:31.456168',6);
INSERT INTO project VALUES(18,'Example Module','Example Description','2023-09-07 15:39:26.953758',6);
INSERT INTO project VALUES(19,'Module 1',replace(replace('Description\r\n','\r',char(13)),'\n',char(10)),'2023-09-07 21:04:49.983505',1);
CREATE TABLE element (
	id INTEGER NOT NULL, 
	name VARCHAR(250) NOT NULL, 
	"desc" VARCHAR(1000), 
	element_type INTEGER NOT NULL, 
	project_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(element_type) REFERENCES type (id), 
	FOREIGN KEY(project_id) REFERENCES project (id)
);
INSERT INTO element VALUES(225,'LO1','',1,1);
INSERT INTO element VALUES(226,'LO2','',1,1);
INSERT INTO element VALUES(227,'LO3','',1,1);
INSERT INTO element VALUES(228,'Con1','',2,1);
INSERT INTO element VALUES(229,'Con2','',2,1);
INSERT INTO element VALUES(230,'Con3','',2,1);
INSERT INTO element VALUES(231,'Con4','',2,1);
INSERT INTO element VALUES(232,'LA1','',3,1);
INSERT INTO element VALUES(233,'LA2','',3,1);
INSERT INTO element VALUES(234,'ASM1','',4,1);
INSERT INTO element VALUES(235,'ASM2','',4,1);
INSERT INTO element VALUES(236,'ASM3','',4,1);
INSERT INTO element VALUES(249,'A','',1,2);
INSERT INTO element VALUES(250,'B','',1,2);
INSERT INTO element VALUES(251,'C','',1,2);
INSERT INTO element VALUES(252,'D','',2,2);
INSERT INTO element VALUES(253,'E','',2,2);
INSERT INTO element VALUES(254,'F','',2,2);
INSERT INTO element VALUES(255,'G','',3,2);
INSERT INTO element VALUES(256,'H','',3,2);
INSERT INTO element VALUES(257,'I','',3,2);
INSERT INTO element VALUES(258,'J','',4,2);
INSERT INTO element VALUES(259,'K','',4,2);
INSERT INTO element VALUES(260,'L','',4,2);
INSERT INTO element VALUES(263,'D','',2,3);
INSERT INTO element VALUES(265,'A','',1,3);
INSERT INTO element VALUES(266,'B','Example desc',1,3);
INSERT INTO element VALUES(267,'C','',1,3);
INSERT INTO element VALUES(268,'E','',2,3);
INSERT INTO element VALUES(269,'F','',2,3);
INSERT INTO element VALUES(270,'G','',3,3);
INSERT INTO element VALUES(271,'H','',3,3);
INSERT INTO element VALUES(272,'I','',3,3);
INSERT INTO element VALUES(273,'J','',4,3);
INSERT INTO element VALUES(274,'K','',4,3);
INSERT INTO element VALUES(275,'L','',4,3);
INSERT INTO element VALUES(276,'1','',1,4);
INSERT INTO element VALUES(277,'2','',3,4);
INSERT INTO element VALUES(278,'A','Description2',1,5);
INSERT INTO element VALUES(279,'B','Description aaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa aaaaaaaaa aaaaaaaaaaaaa aaaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaa aaaaaaaaa',1,5);
INSERT INTO element VALUES(281,'D','',2,5);
INSERT INTO element VALUES(282,'E','',2,5);
INSERT INTO element VALUES(283,'F','',2,5);
INSERT INTO element VALUES(284,'G','',3,5);
INSERT INTO element VALUES(285,'H','',3,5);
INSERT INTO element VALUES(286,'I','',3,5);
INSERT INTO element VALUES(287,'J','',4,5);
INSERT INTO element VALUES(288,'K','',4,5);
INSERT INTO element VALUES(289,'L','',4,5);
INSERT INTO element VALUES(290,'C','',1,5);
INSERT INTO element VALUES(291,'LO1 - Example description of a learning outcome ','Example description of a learning outcome dzfhjsrg,jfbjk,bfjhsbzfjmesgukf,wfjemsbdkulwebdlwebaukdbawdbbdnm',1,6);
INSERT INTO element VALUES(292,'LO2 - Example description of a learning outcome','',1,6);
INSERT INTO element VALUES(293,'LO3 - Example description of a learning outcome','',1,6);
INSERT INTO element VALUES(294,'Topic 1 - introduction','',2,6);
INSERT INTO element VALUES(295,'Topic 2 - Further information','',2,6);
INSERT INTO element VALUES(296,'Topic 3 - Example description of a learning outcome','',2,6);
INSERT INTO element VALUES(297,'Topic 4 - Final thoughts','',2,6);
INSERT INTO element VALUES(298,'Worksheet 0 - Preliminary knowledge','',3,6);
INSERT INTO element VALUES(299,'Worksheet 1 - In class exercise','',3,6);
INSERT INTO element VALUES(300,'Worksheet 2 - Electrical diagrams','',3,6);
INSERT INTO element VALUES(301,'Lab exercise','',3,6);
INSERT INTO element VALUES(302,'Exam 1 - basics of electronics',replace(replace('30%\r\nComputer exam','\r',char(13)),'\n',char(10)),4,6);
INSERT INTO element VALUES(303,'Exam 2 - advanced electronics',replace(replace('30%\r\nPen and paper','\r',char(13)),'\n',char(10)),4,6);
INSERT INTO element VALUES(304,'Essay - my reflection on the exams','40%',4,6);
INSERT INTO element VALUES(305,'LO1','Description of learning outcome',1,7);
INSERT INTO element VALUES(306,'LO2','',1,7);
INSERT INTO element VALUES(307,'LO4','',1,7);
INSERT INTO element VALUES(308,'Lecture 1','',2,7);
INSERT INTO element VALUES(309,'Lecture 2','',2,7);
INSERT INTO element VALUES(310,'Lecture 3','',2,7);
INSERT INTO element VALUES(311,'Lecture 4','',2,7);
INSERT INTO element VALUES(312,'Worksheet 1','',3,7);
INSERT INTO element VALUES(313,'Worksheet 2','',3,7);
INSERT INTO element VALUES(314,'Lab exercise','',3,7);
INSERT INTO element VALUES(315,'Exam 1',replace(replace('30%\r\nPen and paper','\r',char(13)),'\n',char(10)),4,7);
INSERT INTO element VALUES(316,'Exam 2','',4,7);
INSERT INTO element VALUES(317,'Essay','',4,7);
INSERT INTO element VALUES(318,'LO4','Example description of a module. This module will contain lectures. It will maybe also have some work the students can do. ',1,8);
INSERT INTO element VALUES(319,'LO2','',1,8);
INSERT INTO element VALUES(320,'Content 1','',2,8);
INSERT INTO element VALUES(321,'Content 2','An introduction lecture',2,8);
INSERT INTO element VALUES(322,'LA1','',3,8);
INSERT INTO element VALUES(323,'LA2','',3,8);
INSERT INTO element VALUES(324,'LA3','',3,8);
INSERT INTO element VALUES(325,'Exam 1',replace(replace('30%\r\nPen and paper','\r',char(13)),'\n',char(10)),4,8);
INSERT INTO element VALUES(326,'Essay','50%',4,8);
INSERT INTO element VALUES(327,'Lab exercise','',3,6);
INSERT INTO element VALUES(328,'Lab exercise','',3,6);
INSERT INTO element VALUES(329,'Lab exercise','',3,6);
INSERT INTO element VALUES(330,'Lab exercise','',3,6);
INSERT INTO element VALUES(331,'Lab exercise','',3,6);
INSERT INTO element VALUES(332,'Lab exercise','',3,6);
INSERT INTO element VALUES(333,'Lab exercise','',3,6);
INSERT INTO element VALUES(334,'A','',1,9);
INSERT INTO element VALUES(335,'B','',1,9);
INSERT INTO element VALUES(336,'C','',1,9);
INSERT INTO element VALUES(337,'D','',2,9);
INSERT INTO element VALUES(338,'E','',3,9);
INSERT INTO element VALUES(339,'F','',4,9);
INSERT INTO element VALUES(340,'Element','',1,15);
INSERT INTO element VALUES(341,'LO1 - Learning C++ Programming','Learning C++',1,16);
INSERT INTO element VALUES(342,'LO2 - Breadboarding skills',replace(replace('Building Breadboards\r\n','\r',char(13)),'\n',char(10)),1,16);
INSERT INTO element VALUES(343,'LO3 - Understanding sensors','Using and testing sensors',1,16);
INSERT INTO element VALUES(344,'C++ Programming',replace(replace('Programming for Arduino\r\n','\r',char(13)),'\n',char(10)),2,16);
INSERT INTO element VALUES(345,'GPIO Components','',2,16);
INSERT INTO element VALUES(346,'Interfacing with components','',2,16);
INSERT INTO element VALUES(347,'In class test - programming','Programming on C++',4,16);
INSERT INTO element VALUES(348,'In class test - breadboarding','',4,16);
INSERT INTO element VALUES(349,'Coursework - C++','',4,16);
INSERT INTO element VALUES(350,'Lab session 1','3 hours - Basic microcontrollers',3,16);
INSERT INTO element VALUES(351,'Lab session 2','Variables and operators',3,16);
INSERT INTO element VALUES(352,'Lab session 3','Branches',3,16);
INSERT INTO element VALUES(353,'Learning outcome 1','Example desc',1,17);
INSERT INTO element VALUES(354,'Learning outcome 2','',1,17);
INSERT INTO element VALUES(355,'Learning outcome 3','',1,17);
INSERT INTO element VALUES(356,'Content 1','',2,17);
INSERT INTO element VALUES(357,'Content 2','',2,17);
INSERT INTO element VALUES(358,'Content 3','',2,17);
INSERT INTO element VALUES(359,'Content 4','',2,17);
INSERT INTO element VALUES(360,'Learning activity 0','Pre-requisite knowledge',3,17);
INSERT INTO element VALUES(361,'Learning activity 2','',3,17);
INSERT INTO element VALUES(362,'Learning activity 3','',3,17);
INSERT INTO element VALUES(363,'Assessment 1','Exam - 50%',4,17);
INSERT INTO element VALUES(364,'Assessment 2','Essay - 50%',4,17);
INSERT INTO element VALUES(365,'Understanding Design Fundamentals','Develop a solid foundation in design principles, aesthetics, and human-centred design concepts to effectively analyse and critique product designs.',1,18);
INSERT INTO element VALUES(366,'Design Research and User-Centred Design','Learn to conduct user research, identify user needs, and apply user-centred design methodologies to create products that meet real-world user requirements.',1,18);
INSERT INTO element VALUES(367,'Prototyping and Materials Selection','Gain proficiency in prototyping techniques, material selection, and manufacturing processes to create physical and digital prototypes that align with design goals and constraints.',1,18);
INSERT INTO element VALUES(368,'Design for Sustainability','Explore sustainable design principles, environmental considerations, and ethical practices in product design, aiming to minimise ecological impact and promote responsible production.',1,18);
INSERT INTO element VALUES(369,'Project Management and Design Entrepreneurship','Develop project management skills, learn to create design briefs, budgets, and business plans, and understand the entrepreneurial aspects of bringing a product to market.',1,18);
INSERT INTO element VALUES(370,'Design History and Theory','Explore the evolution of design through history and delve into design theories, movements, and influential designers to gain a comprehensive understanding of design''s cultural and historical context.',2,18);
INSERT INTO element VALUES(371,'User Research and Persona Development','Learn the methodologies of conducting user research, including surveys, interviews, and observations, and use the collected data to create detailed user personas that inform the design process.',2,18);
INSERT INTO element VALUES(372,'Sketching and Digital Design Tools','Develop proficient sketching skills both by hand and using digital tools, enabling you to visually communicate design ideas effectively, from initial concepts to detailed renderings.',2,18);
INSERT INTO element VALUES(373,'Materials Science and Selection','Study the science behind materials used in product design, including their properties, sustainability aspects, and environmental impact, and learn how to make informed choices when selecting materials for specific design applications.',2,18);
INSERT INTO element VALUES(374,'Prototyping Techniques (3D Printing, CAD, etc.)','Explore a variety of prototyping techniques, such as 3D printing, computer-aided design (CAD), and other digital tools, to create functional and visually representative prototypes for design validation and iteration.',2,18);
INSERT INTO element VALUES(375,'Human Factors and Ergonomics','Investigate the principles of human factors and ergonomics to design products that are comfortable, safe, and user-friendly by considering the physical and psychological needs of end-users.',2,18);
INSERT INTO element VALUES(376,'Sustainable Design Practices','Dive into sustainable design practices, including eco-friendly materials, energy-efficient design, and sustainable manufacturing processes, with a focus on minimising environmental impact throughout the product''s lifecycle.',2,18);
INSERT INTO element VALUES(377,'Design Ethics and Intellectual Property','Examine ethical considerations in product design, including issues related to intellectual property, privacy, and social responsibility, fostering a responsible and ethical approach to design innovation.',2,18);
INSERT INTO element VALUES(378,'Design Critique Workshop','Students participate in group discussions to analyse and critique existing product designs, applying design principles learned in class.',3,18);
INSERT INTO element VALUES(379,'User Interviews and Persona Creation','Students conduct interviews with potential users and create detailed personas to inform their design projects.',3,18);
INSERT INTO element VALUES(380,'Sketching and Ideation Sessions','Creative brainstorming sessions and sketching exercises to explore design concepts and refine ideas.',3,18);
INSERT INTO element VALUES(381,'Prototyping Workshops','Hands-on sessions to learn various prototyping techniques, from paper prototypes to 3D printing, to bring designs to life.',3,18);
INSERT INTO element VALUES(382,'Material Selection Lab','Students experiment with different materials and manufacturing processes, making informed choices for their design projects.',3,18);
INSERT INTO element VALUES(383,'Usability Testing and Feedback Sessions','Conduct user testing to gather feedback on prototypes and refine designs based on user input.',3,18);
INSERT INTO element VALUES(384,'Sustainability Assessment Project','Students analyse a product''s lifecycle and environmental impact, proposing sustainable design improvements.',3,18);
INSERT INTO element VALUES(385,'Business Plan and Pitch Simulation','Develop a business plan for a product design concept and present it to a panel, simulating the process of seeking funding or entrepreneurship.',3,18);
INSERT INTO element VALUES(386,'Design Exhibition','Showcase final product designs in a university-wide design exhibition, allowing students to present their work to a broader audience.',3,18);
INSERT INTO element VALUES(387,'Design Ethics Seminar','Engage in discussions and case studies on ethical considerations in product design, encouraging responsible and ethical design practices.',3,18);
INSERT INTO element VALUES(388,'Design Portfolio Review','Students will compile a comprehensive portfolio showcasing their design projects, reflecting their growth in design skills, creativity, and understanding of user-centred design principles.',4,18);
INSERT INTO element VALUES(389,'Prototype Evaluation and Presentation','Students will compile a comprehensive portfolio showcasing their design projects, reflecting their growth in design skills, creativity, and understanding of user-centred design principles.',4,18);
INSERT INTO element VALUES(390,'Design Case Study and Sustainability Analysis','Students will conduct a case study on a product, evaluating its sustainability features and proposing improvements, highlighting their grasp of sustainable design principles.',4,18);
INSERT INTO element VALUES(391,'Guest Lectures and Industry Visits','Invite guest speakers from the design industry and organise visits to design studios or manufacturing facilities to gain real-world insights into product design processes.',3,18);
INSERT INTO element VALUES(392,'LO1','',1,19);
INSERT INTO element VALUES(393,'LO2','',1,19);
INSERT INTO element VALUES(394,'LO3 - Understanding sensors','',1,19);
INSERT INTO element VALUES(395,'Custard','',2,19);
INSERT INTO element VALUES(396,'Jam','',2,19);
INSERT INTO element VALUES(397,'Donuts making','',3,19);
INSERT INTO element VALUES(398,'donut filling','',3,19);
INSERT INTO element VALUES(399,'dunought eating','',3,19);
INSERT INTO element VALUES(400,'Taste exam','',4,19);
INSERT INTO element VALUES(401,'Texture coursework','',4,19);
INSERT INTO element VALUES(402,'Essay on desserts','',4,19);
CREATE TABLE connection (
	id INTEGER NOT NULL, 
	project_id INTEGER NOT NULL, 
	element1 INTEGER NOT NULL, 
	element2 INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(project_id) REFERENCES project (id), 
	FOREIGN KEY(element1) REFERENCES element (id), 
	FOREIGN KEY(element2) REFERENCES element (id)
);
INSERT INTO connection VALUES(1,5,278,284);
INSERT INTO connection VALUES(3,5,284,282);
INSERT INTO connection VALUES(4,5,286,281);
INSERT INTO connection VALUES(6,5,286,283);
INSERT INTO connection VALUES(7,5,279,285);
INSERT INTO connection VALUES(8,5,278,286);
INSERT INTO connection VALUES(10,5,282,289);
INSERT INTO connection VALUES(16,5,289,279);
INSERT INTO connection VALUES(17,5,289,278);
INSERT INTO connection VALUES(18,5,285,281);
INSERT INTO connection VALUES(19,1,227,233);
INSERT INTO connection VALUES(20,1,232,230);
INSERT INTO connection VALUES(21,5,283,288);
INSERT INTO connection VALUES(24,5,281,288);
INSERT INTO connection VALUES(25,6,293,301);
INSERT INTO connection VALUES(26,6,293,300);
INSERT INTO connection VALUES(27,6,291,298);
INSERT INTO connection VALUES(28,6,292,298);
INSERT INTO connection VALUES(29,6,293,299);
INSERT INTO connection VALUES(30,6,301,296);
INSERT INTO connection VALUES(31,6,300,295);
INSERT INTO connection VALUES(32,6,299,294);
INSERT INTO connection VALUES(33,6,298,294);
INSERT INTO connection VALUES(34,6,294,302);
INSERT INTO connection VALUES(35,6,295,302);
INSERT INTO connection VALUES(36,6,296,303);
INSERT INTO connection VALUES(37,6,304,297);
INSERT INTO connection VALUES(38,6,302,291);
INSERT INTO connection VALUES(39,6,303,291);
INSERT INTO connection VALUES(40,6,303,292);
INSERT INTO connection VALUES(41,6,303,293);
INSERT INTO connection VALUES(42,6,295,303);
INSERT INTO connection VALUES(43,6,304,293);
INSERT INTO connection VALUES(44,7,305,312);
INSERT INTO connection VALUES(45,7,307,313);
INSERT INTO connection VALUES(46,7,306,314);
INSERT INTO connection VALUES(47,7,312,309);
INSERT INTO connection VALUES(48,7,313,311);
INSERT INTO connection VALUES(49,7,314,308);
INSERT INTO connection VALUES(50,7,308,316);
INSERT INTO connection VALUES(51,7,309,315);
INSERT INTO connection VALUES(52,7,310,315);
INSERT INTO connection VALUES(53,7,311,315);
INSERT INTO connection VALUES(54,7,315,306);
INSERT INTO connection VALUES(55,7,316,307);
INSERT INTO connection VALUES(57,8,319,323);
INSERT INTO connection VALUES(61,8,321,325);
INSERT INTO connection VALUES(63,9,335,338);
INSERT INTO connection VALUES(64,9,338,337);
INSERT INTO connection VALUES(65,9,339,337);
INSERT INTO connection VALUES(66,9,339,334);
INSERT INTO connection VALUES(67,9,339,335);
INSERT INTO connection VALUES(77,8,319,325);
INSERT INTO connection VALUES(80,8,320,326);
INSERT INTO connection VALUES(82,8,319,326);
INSERT INTO connection VALUES(86,8,324,321);
INSERT INTO connection VALUES(87,8,323,321);
INSERT INTO connection VALUES(88,9,336,339);
INSERT INTO connection VALUES(89,16,347,341);
INSERT INTO connection VALUES(90,16,342,348);
INSERT INTO connection VALUES(91,16,342,349);
INSERT INTO connection VALUES(92,16,341,349);
INSERT INTO connection VALUES(93,16,343,349);
INSERT INTO connection VALUES(94,16,351,341);
INSERT INTO connection VALUES(95,16,341,352);
INSERT INTO connection VALUES(96,16,344,351);
INSERT INTO connection VALUES(97,16,344,352);
INSERT INTO connection VALUES(98,16,344,349);
INSERT INTO connection VALUES(99,16,344,347);
INSERT INTO connection VALUES(100,17,353,360);
INSERT INTO connection VALUES(101,17,353,361);
INSERT INTO connection VALUES(102,17,354,362);
INSERT INTO connection VALUES(103,17,360,357);
INSERT INTO connection VALUES(104,17,360,358);
INSERT INTO connection VALUES(105,17,360,359);
INSERT INTO connection VALUES(106,17,361,358);
INSERT INTO connection VALUES(107,17,362,359);
INSERT INTO connection VALUES(108,17,364,359);
INSERT INTO connection VALUES(109,17,363,358);
INSERT INTO connection VALUES(110,17,363,353);
INSERT INTO connection VALUES(111,17,363,354);
INSERT INTO connection VALUES(112,17,364,354);
INSERT INTO connection VALUES(113,17,364,355);
INSERT INTO connection VALUES(114,17,357,363);
INSERT INTO connection VALUES(115,18,365,378);
INSERT INTO connection VALUES(116,18,365,379);
INSERT INTO connection VALUES(117,18,366,380);
INSERT INTO connection VALUES(118,18,366,381);
INSERT INTO connection VALUES(119,18,366,382);
INSERT INTO connection VALUES(120,18,367,384);
INSERT INTO connection VALUES(121,18,367,386);
INSERT INTO connection VALUES(122,18,368,387);
INSERT INTO connection VALUES(123,18,378,371);
INSERT INTO connection VALUES(124,18,370,379);
INSERT INTO connection VALUES(125,18,379,373);
INSERT INTO connection VALUES(126,18,381,372);
INSERT INTO connection VALUES(127,18,375,382);
INSERT INTO connection VALUES(128,18,384,374);
INSERT INTO connection VALUES(129,18,376,386);
INSERT INTO connection VALUES(130,18,377,380);
INSERT INTO connection VALUES(131,18,378,377);
INSERT INTO connection VALUES(132,18,390,377);
INSERT INTO connection VALUES(133,18,377,389);
INSERT INTO connection VALUES(134,18,373,389);
INSERT INTO connection VALUES(135,18,389,374);
INSERT INTO connection VALUES(136,18,374,388);
INSERT INTO connection VALUES(137,18,388,371);
INSERT INTO connection VALUES(138,18,370,388);
INSERT INTO connection VALUES(139,18,388,372);
INSERT INTO connection VALUES(140,18,390,369);
INSERT INTO connection VALUES(141,18,389,368);
INSERT INTO connection VALUES(142,18,389,367);
INSERT INTO connection VALUES(143,18,389,366);
INSERT INTO connection VALUES(144,18,389,369);
INSERT INTO connection VALUES(145,18,388,366);
INSERT INTO connection VALUES(146,19,394,397);
INSERT INTO connection VALUES(147,19,392,397);
INSERT INTO connection VALUES(148,19,393,398);
INSERT INTO connection VALUES(149,19,397,395);
INSERT INTO connection VALUES(150,19,398,396);
INSERT INTO connection VALUES(151,19,398,395);
INSERT INTO connection VALUES(152,19,395,400);
INSERT INTO connection VALUES(153,19,396,401);
INSERT INTO connection VALUES(154,19,402,394);
INSERT INTO connection VALUES(155,19,401,393);
INSERT INTO connection VALUES(156,19,400,392);
INSERT INTO connection VALUES(157,19,399,396);
CREATE TABLE access (
	id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	project_id INTEGER NOT NULL, 
	access_level INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id), 
	FOREIGN KEY(project_id) REFERENCES project (id)
);
INSERT INTO access VALUES(2,3,8,2);
INSERT INTO access VALUES(3,1,9,2);
INSERT INTO access VALUES(4,3,9,2);
INSERT INTO access VALUES(5,1,11,1);
INSERT INTO access VALUES(6,1,12,1);
INSERT INTO access VALUES(7,3,16,2);
INSERT INTO access VALUES(8,3,17,1);
COMMIT;
