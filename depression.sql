-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Dec 18, 2024 at 10:02 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `depression`
--

-- --------------------------------------------------------

--
-- Table structure for table `dp_login`
--

CREATE TABLE `dp_login` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dp_login`
--

INSERT INTO `dp_login` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `dp_medication`
--

CREATE TABLE `dp_medication` (
  `id` int(11) NOT NULL,
  `dtype` varchar(50) NOT NULL,
  `stage` varchar(20) NOT NULL,
  `medication` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dp_medication`
--

INSERT INTO `dp_medication` (`id`, `dtype`, `stage`, `medication`) VALUES
(1, 'Major Depressive Disorder', 'Very Mild', 'Getting quality sleep and having a healthy sleep routine.'),
(2, 'Major Depressive Disorder', 'Mild', 'Managing stress with healthy coping mechanisms.'),
(3, 'Major Depressive Disorder', 'Moderate', 'Practicing regular self-care activities such as exercise, meditation and yoga.'),
(4, 'Major Depressive Disorder', 'Severe', 'Managing any underlying medical or mental health conditions you have. Avoiding misuse of alcohol and other substances.'),
(5, 'Persistent Depressive Disorder', 'Very Mild', 'Take steps to control stress, to increase your ability to recover from problems — which is called resilience and to boost your self-esteem.'),
(6, 'Persistent Depressive Disorder', 'Mild', 'Reach out to family and friends, especially in times of crisis, to help you get through rough spells.'),
(7, 'Persistent Depressive Disorder', 'Moderate', 'Get treatment at the earliest sign of a problem to help prevent symptoms from worsening.'),
(8, 'Persistent Depressive Disorder', 'Severe', 'Consider getting long-term treatment to help prevent a relapse of symptoms.'),
(9, 'Bipolar Disorder', 'Very Mild', 'Medications, Self-management strategies, like education and identifying the early symptoms of an episode or possible triggers of episodes. Helpful lifestyle habits, such as exercise, yoga and meditation. These can support, but not replace, treatment.'),
(10, 'Bipolar Disorder', 'Mild', 'Medications, Self-management strategies, like education and identifying the early symptoms of an episode or possible triggers of episodes. Helpful lifestyle habits, such as exercise, yoga and meditation. These can support, but not replace, treatment.'),
(11, 'Bipolar Disorder', 'Moderate', 'Medications, Self-management strategies, like education and identifying the early symptoms of an episode or possible triggers of episodes. Helpful lifestyle habits, such as exercise, yoga and meditation. These can support, but not replace, treatment.'),
(12, 'Bipolar Disorder', 'Severe', 'Medications, Self-management strategies, like education and identifying the early symptoms of an episode or possible triggers of episodes. Helpful lifestyle habits, such as exercise, yoga and meditation. These can support, but not replace, treatment.');

-- --------------------------------------------------------

--
-- Table structure for table `dp_question`
--

CREATE TABLE `dp_question` (
  `id` int(11) NOT NULL,
  `question` varchar(200) NOT NULL,
  `skey` varchar(30) NOT NULL,
  `answer` int(11) NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dp_question`
--

INSERT INTO `dp_question` (`id`, `question`, `skey`, `answer`, `status`) VALUES
(1, 'Changes in weight', 'a2', 2, 1),
(2, 'Difficulty falling or staying asleep', 'b1', 3, 1),
(3, 'Thoughts of death and suicide', 'a4', 4, 1),
(4, 'Fatigue, insomnia, and lethargy', 'c3', 3, 1),
(5, 'Lack of interest in activities normally enjoyed', 'a1', 2, 1),
(6, 'Difficulty concentrating', 'a3', 4, 1),
(7, 'Feelings of hopelessness', 'b3', 3, 1),
(8, 'Indecision and disorganization', 'c4', 3, 1),
(9, 'Feelings of guilt', 'b2', 2, 1),
(10, 'Loss of interest and pleasure', 'b4', 4, 1),
(11, 'Agitation', 'h1', 3, 1),
(12, 'Strongly reactive moods', 'g4', 2, 1),
(13, 'Excessive sleep', 'g1', 1, 1),
(14, 'Insomnia', 'h3', 4, 1),
(15, 'Frequent oversleeping', 'f2', 3, 1),
(16, 'Relationship problems', 'f4', 1, 1),
(17, 'Intense sensitivity to rejection', 'g3', 2, 1),
(18, 'Food cravings or binging', 'e4', 2, 1),
(19, 'Heaviness in arms and legs', 'f1', 3, 1),
(20, 'Constipation', 'h2', 0, 1),
(21, 'Social withdrawal', 'd2', 0, 1),
(22, 'Extreme fatigue', 'e1', 2, 1),
(23, 'Thoughts of hurting yourself or your baby', 'd4', 0, 1),
(24, 'Intellectual impairment', 'h4', 4, 1),
(25, 'Unexplained aches, pains, and psychomotor agitation', 'c1', 3, 1),
(26, 'Cravings for carbohydrates/weight gain', 'f3', 2, 1),
(27, 'Severe mood swings', 'd1', 4, 1),
(28, 'Irritability', 'e3', 2, 1),
(29, 'Fatigue, weakness, and feeling "weighed down"', 'g2', 3, 1),
(30, 'Hopelessness and loss of self-esteem', 'c2', 3, 1),
(31, 'Appetite changes', 'd3', 2, 1),
(32, 'Severe feelings of stress or anxiety', 'e2', 0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `dp_recommend`
--

CREATE TABLE `dp_recommend` (
  `id` int(11) NOT NULL,
  `hospital` varchar(30) NOT NULL,
  `specialist` varchar(50) NOT NULL,
  `av_time` varchar(30) NOT NULL,
  `address` varchar(50) NOT NULL,
  `city` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dp_recommend`
--

INSERT INTO `dp_recommend` (`id`, `hospital`, `specialist`, `av_time`, `address`, `city`, `mobile`, `email`) VALUES
(1, 'Wellcare Hospital', 'Dr.Sivaraman', '10am to 3pm', 'Thillai Nagar', 'Trichy', 9638845677, 'sivaraman@gmail.com'),
(2, 'Chitra Hospital', 'Dr.Chitradevi Priya', '9am to 2pm', 'Valayapettai Agraharam', 'Kumbakonam', 8800017445, 'chitra@gmail.com'),
(3, 'Madhu Hospital', 'Dr.Madhumathi Shanmugasundaram', '3pm to 8pm', 'K.K Nagar', 'Madurai', 9975811245, 'madhumathis@gmail.com'),
(4, 'Jayaram Hospital', 'Dr.Vasantha Jayaram', '10am to 2pm', 'D.Nagar', 'Chennai', 8896711247, 'vasanthajr@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `dp_result`
--

CREATE TABLE `dp_result` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `test_id` int(11) NOT NULL,
  `depression_level` varchar(20) NOT NULL,
  `depression_type` varchar(50) NOT NULL,
  `date_time` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dp_result`
--

INSERT INTO `dp_result` (`id`, `uname`, `test_id`, `depression_level`, `depression_type`, `date_time`) VALUES
(1, 'dinesh', 1, 'Mild', 'Major Depressive Disorder', '2023-12-04 15:31:38'),
(2, 'dinesh', 2, 'Very Mild', 'Major Depressive Disorder', '2023-12-04 20:00:45'),
(3, '', 3, 'Mild', 'Psychotic Depression', '2024-03-17 15:58:53'),
(4, 'ravi', 4, 'Severe', 'Seasonal Affective Disorder', '2024-03-18 01:13:54');

-- --------------------------------------------------------

--
-- Table structure for table `dp_test`
--

CREATE TABLE `dp_test` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `age` int(11) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `value1` int(11) NOT NULL,
  `value2` int(11) NOT NULL,
  `value3` int(11) NOT NULL,
  `value4` int(11) NOT NULL,
  `value5` int(11) NOT NULL,
  `value6` int(11) NOT NULL,
  `value7` int(11) NOT NULL,
  `value8` int(11) NOT NULL,
  `value9` int(11) NOT NULL,
  `value10` int(11) NOT NULL,
  `value11` int(11) NOT NULL,
  `value12` int(11) NOT NULL,
  `value13` int(11) NOT NULL,
  `value14` int(11) NOT NULL,
  `value15` int(11) NOT NULL,
  `value16` int(11) NOT NULL,
  `value17` int(11) NOT NULL,
  `value18` int(11) NOT NULL,
  `value19` int(11) NOT NULL,
  `value20` int(11) NOT NULL,
  `value21` int(11) NOT NULL,
  `value22` int(11) NOT NULL,
  `value23` int(11) NOT NULL,
  `value24` int(11) NOT NULL,
  `value25` int(11) NOT NULL,
  `value26` int(11) NOT NULL,
  `value27` int(11) NOT NULL,
  `value28` int(11) NOT NULL,
  `value29` int(11) NOT NULL,
  `value30` int(11) NOT NULL,
  `value31` int(11) NOT NULL,
  `value32` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dp_test`
--

INSERT INTO `dp_test` (`id`, `uname`, `age`, `gender`, `value1`, `value2`, `value3`, `value4`, `value5`, `value6`, `value7`, `value8`, `value9`, `value10`, `value11`, `value12`, `value13`, `value14`, `value15`, `value16`, `value17`, `value18`, `value19`, `value20`, `value21`, `value22`, `value23`, `value24`, `value25`, `value26`, `value27`, `value28`, `value29`, `value30`, `value31`, `value32`) VALUES
(1, 'dinesh', 35, 'Male', 2, 2, 2, 1, 1, 0, 2, 0, 0, 0, 2, 0, 0, 2, 1, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0),
(2, 'dinesh', 28, 'Male', 1, 1, 2, 2, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 4, 0, 0, 0, 0, 3, 1, 0, 0, 0, 2, 0),
(3, '', 58, 'Male', 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 2, 0, 0, 2, 0, 2, 0, 0, 2, 0, 2, 2, 2, 2, 1),
(4, 'ravi', 38, 'Male', 4, 1, 3, 0, 3, 3, 1, 3, 0, 3, 0, 2, 2, 0, 4, 3, 0, 0, 0, 3, 4, 3, 4, 0, 3, 0, 0, 0, 0, 2, 2, 4);

-- --------------------------------------------------------

--
-- Table structure for table `dp_treatment`
--

CREATE TABLE `dp_treatment` (
  `id` int(11) NOT NULL,
  `dtype` varchar(50) NOT NULL,
  `life_time` text NOT NULL,
  `treatment` text NOT NULL,
  `medication` text NOT NULL,
  `suggestion` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dp_treatment`
--

INSERT INTO `dp_treatment` (`id`, `dtype`, `life_time`, `treatment`, `medication`, `suggestion`) VALUES
(1, 'Major Depressive Disorder', 'Getting quality sleep and having a healthy sleep routine.\r\nManaging stress with healthy coping mechanisms.\r\nPracticing regular self-care activities such as exercise, meditation and yoga.\r\nManaging any underlying medical or mental health conditions you have.\r\nAvoiding misuse of alcohol and other substances.', 'Psychotherapy', 'Selective Serotonin Reuptake Inhibitors (SSRI)\r\nSerotonin and Norepinephrine Reuptake Inhibitors (SNRI)\r\nTricyclic and Tetracyclic Antidepressants.\r\nAtypical Antidepressants.', 'Your primary care doctor or psychiatrist can prescribe medications to relieve symptoms. However, many people with depression also benefit from seeing a psychiatrist, psychologist or other mental health professional.'),
(2, 'Persistent Depressive Disorder', 'Take steps to control stress, to increase your ability to recover from problems — which is called resilience — and to boost your self-esteem.<br>Reach out to family and friends, especially in times of crisis, to help you get through rough spells.<br>Get treatment at the earliest sign of a problem to help prevent symptoms from worsening.<br>Consider getting long-term treatment to help prevent a relapse of symptoms.', 'Psychotherapy', 'Selective serotonin reuptake inhibitors (SSRIs)<br>\r\nTricyclic antidepressants (TCAs)<br>\r\nSerotonin and norepinephrine reuptake inhibitors (SNRIs)', 'Persistent depressive disorder is a continuous, long-term form of depression. You may feel sad and empty, lose interest in daily activities and have trouble getting things done. You may also have low self-esteem, feel like a failure and feel hopeless.'),
(3, 'Bipolar Disorder', 'Quit drinking alcohol and/or using recreational drugs and tobacco: It’s essential to quit drinking and using drugs, including tobacco, since they can interfere with medications you may take. They can also worsen bipolar disorder and trigger a mood episode.\r\nKeep a daily diary or mood chart: Keeping track of your daily thoughts, feelings and behaviors can help you be aware of how well your treatment is working and/or help you identify potential triggers of manic or depressive episodes.\r\nMaintain a healthy sleep schedule: Bipolar disorder can greatly affect your sleep patterns, and changes in your frequency of sleep can even trigger an episode. Prioritize a routine sleeping schedule, including going to sleep and getting up at the same times every day.\r\n<Exercise: Exercise has been proven to improve mood and mental health in general, so it may help manage your symptoms related to bipolar disorder. Since weight gain is a common side effect of bipolar disorder medications, exercise may also help with weight management.\r\nMeditation: Meditation has been shown to be effective in improving the depression that’s part of bipolar disorder.\r\n<br>Manage stress and maintain healthy relationships: Stress and anxiety can worsen mood symptoms in many people with bipolar disorder. It’s important to manage your stress in a healthy way and to try to eliminate stressors when you can. A big part of this is maintaining healthy relationships with friends and family who support you, and letting go of toxic relationships with people who add stress to your life.', 'Psychotherapy (talk therapy).<br>Medications.<br>Self-management strategies, like education and identifying the early symptoms of an episode or possible triggers of episodes.<br>\r\nHelpful lifestyle habits, such as exercise, yoga and meditation. These can support, but not replace, treatment.<br>Other therapies, such as electroconvulsive therapy (ECT) in cases that are poorly responsive to medication or where rapid control of symptoms is necessary to prevent harm.', 'Fluoxetine combined with olanzapine (Symbyax)<br>\r\nlumateperone (Caplyta)<br>\r\nLurasidone (Latuda)', 'Mayo Clinic has one of the largest and most experienced practice in the United States, with campuses in Arizona, Florida and Minnesota. Staff skilled in dozens of specialties work together to ensure quality care and successful recovery.'),
(4, 'Postpartum Depression', 'Exercise when you can<br>\r\nMaintain a healthy diet<br>\r\nCreate time for yourself<br>\r\nMake time to rest<br>\r\nExamine your breast-feeding', 'Postpartum depression is treated differently depending on the type and severity of your symptoms. Treatment options include anti-anxiety or antidepressant medicines, psychotherapy (talk therapy or cognitive behavioral therapy) and support group participation.<br>Treatment for postpartum psychosis may include medication to treat depression, anxiety and psychosis. You may also be admitted to a treatment center for several days until you''re stable. If you don''t respond to this treatment, electroconvulsive therapy (ECT) can be effective.', 'Selective serotonin reuptake inhibitors (SSRIs) such as sertraline (Zoloft) and fluoxetine.<br>\r\nSerotonin and norepinephrine reuptake inhibitors (SNRIs) such as duloxetine (Cymbalta) and desvenlafaxine.<br>Bupropion (Wellbutrin or Zyban).<br>\r\nTricyclic antidepressants (TCAs) such as amitriptyline (Elavil) or imipramine (Tofranil).', 'Postpartum depression is a mental health illness that affects women after giving birth. For some women, it is normal to feel the “baby blues” for a week or two after giving birth. With postpartum depression, feelings of sadness, loneliness, worthlessness, restlessness, and anxiety may last longer than two weeks.'),
(5, 'Premenstrual Dysphoric Disorder', 'lower quality of life,<br>\r\nincreased absenteeism from work,<br>\r\ndecreased work productivity,<br>\r\nimpaired relationships with others,<br>\r\nincreased visits to health providers', 'Changes in diet to increase protein and carbohydrates and decrease sugar, salt, caffeine, and alcohol<br>Regular exercise<br>Stress management<br>Vitamin supplements (such as vitamin B6, calcium, and magnesium)<br>Anti-inflammatory medicines<br>Selective serotonin reuptake inhibitors (SSRI)<br>Birth control pills', 'premenstrual insomnia. Serotonin Reuptake Inhibitors (SRIs): SRIs have been proven to be effective in the treatment of severe mood and somatic symptoms of PMDD.<br>Benzodiazepines (BZDs): BZDs like alprazolam have been found to be effective only in women with severe anxiety', 'Both PMDD and PMS may cause bloating, breast tenderness, fatigue, and changes in sleep and eating habits. In PMDD , however, at least one of these emotional and behavioral symptoms stands out: Sadness or hopelessness. Anxiety or tension.'),
(6, 'Seasonal Affective Disorder', 'They can no longer adjust to seasonal changes in day length,<br>\r\nleading to sleep,<br>\r\ndont moodup,<br>\r\nbehavior changes', 'A number of treatments are available for seasonal affective disorder (SAD), including cognitive behavioural therapy (CBT), antidepressants and light therapy. A GP will recommend the most suitable treatment option for you, based on the nature and severity of your symptoms.', 'Selective serotonin reuptake inhibitors (SSRIs)<br>\r\nbupropion (Wellbutrin XL, Aplenzin)', 'Seasonal affective disorder or SAD is a recurrent major depressive disorder with a seasonal pattern usually beginning in fall and continuing into winter months. A subsyndromal type of SAD, or S-SAD, is commonly known as “winter blues.” Less often, SAD causes depression in the spring or early summer.'),
(7, 'Atypical Depression', 'person don’t feels.<br>\r\nThink anything.<br>\r\nhandles daily activities such as sleeping, eating, or working.', 'Atypical depression often responds well to treatment. Your treatment may vary depending on the condition’s severity. Treatments for atypical depression usually include psychotherapy (talk therapy) and/or medication.<br>Lifestyle changes, such as exercising regularly or quitting alcohol or recreational drug use, can also help improve symptoms.', 'Nardil (phenelzine)<br>Parnate (tranylcypromine)<br>Marplan (isocarboxazid)<br>Emsam (selegiline)', 'Atypical depression is a type of depression in which you experience a temporary boost in mood in response to positive events. Other symptoms specific to atypical depression include increased appetite, hypersomnia and rejection sensitivity. It''s treatable with psychotherapy and antidepressants.'),
(8, 'Psychotic Depression', 'dont moodup,<br>behavior changes.<br>Exercise when you can<br>Maintain a healthy diet<br>Daily morning exercise and yoga practise', 'Treatment for psychotic depression is given in a hospital setting. That way, the patient has close monitoring by mental health professionals. Different medications are used to stabilize the person''s mood, typically including combinations of antidepressants and antipsychotic medications.', 'escitalopram (Lexapro), fluoxetine (Prozac), paroxetine (Paxil, Pexeva)', 'As long as there is no danger to the client or to others, you can treat psychosis at home. Using an evidenced based approach to identify the underlying issues causing the illness and building a structured care plan is the first step to effective psychosis treatment at home.'),
(9, 'Bipolar Disorder', 'ccc', 'ccx', 'cxx', 'sfsdfd');

-- --------------------------------------------------------

--
-- Table structure for table `dp_user`
--

CREATE TABLE `dp_user` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `address` varchar(50) NOT NULL,
  `city` varchar(30) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `dp_user`
--

INSERT INTO `dp_user` (`id`, `name`, `mobile`, `email`, `address`, `city`, `uname`, `pass`) VALUES
(1, 'Dinesh', 8954513255, 'dinesh@gmail.com', '25, RR Street', 'Salem', 'dinesh', '123456'),
(2, 'Ravi', 9855423114, 'ravi@gmail.com', '25/7 SS Road', 'Salem', 'ravi', '123456');
