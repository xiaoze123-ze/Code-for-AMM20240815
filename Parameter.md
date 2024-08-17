1. **Passenger flow data**

![image](https://github.com/user-attachments/assets/17db162a-84da-4458-8c4d-82b8fe3ff531)


2. **The candidate path set of each od pair**

   (1, 5): (1, 2, 6, 5), (1, 3, 5)

   (1, 6): (1, 2, 6), (1, 3, 6)

   (1, 7): (1, 2, 6, 7), (1, 3, 7)

   (1, 8): (1, 2, 8), (1, 3, 6, 8)

   (1, 9): (1, 2, 9), (1, 3, 6, 9)

   (2, 5): (2, 6, 5), (2, 3, 5)

   (2, 7): (2, 6, 7), (2, 3, 7)

   (3, 8): (3, 6, 8), (3, 2, 8)

   (3, 9): (3, 6, 9), (3, 2, 9)

   (4, 5): (4, 3, 5), (4, 2, 6, 5)

   (4, 6): (4, 3, 6), (4, 2, 6)

   (4, 7): (4, 3, 7), (4, 2, 6, 7)

   (4, 8): (4, 2, 8), (4, 3, 6, 8)

   (4, 9): (4, 3, 6, 9), (4, 2, 9)

   (5, 1): (5, 6, 2, 1), (5, 3, 1)

   (5, 2): (5, 6, 2), (5, 3, 2)

   (5, 4): (5, 3, 4), (5, 6, 2, 4)

   (5, 8): (5, 6, 8), (5, 3, 2, 8)

   (5, 9): (5, 6, 9), (5, 3, 2, 9)

   (6, 1): (6, 2, 1), (6, 3, 1)

   (6, 4): (6, 3, 4), (6, 2, 4)

   (7, 1): (7, 3, 1), (7, 6, 2, 1)

   (7, 2): (7, 6, 2), (7, 3, 2)

   (7, 4): (7, 3, 4), (7, 6, 2, 4)

   (7, 8): (7, 3, 2, 8), (7, 6, 8)

   (7, 9): (7, 6, 9), (7, 3, 2, 9)

   (8, 1): (8, 2, 1), (8, 6, 3, 1)

   (8, 3): (8, 2, 3), (8, 6, 3)

   (8, 4): (8, 2, 4), (8, 6, 3, 4)

   (8, 5): (8, 6, 5), (8, 2, 3, 5)

   (8, 7): (8, 6, 7), (8, 2, 3, 7)

   (9, 1): (9, 2, 1), (9, 6, 3, 1)

   (9, 3): (9, 6, 3), (9, 2, 3)

   (9, 4): (9, 6, 3, 4), (9, 2, 4)

   (9, 5): (9, 6, 5), (9, 2, 3, 5)

   (9, 7): (9, 6, 7), (9, 2, 3, 7)

3. **The parameters related to timetable**

   (1) Only the lengths of sections (2,3) and (3,2) are set to 2.5d, and the lengths of the others are set to d.

   (2) If the length of a section is 2.5d, the lower and upper limit of the train running time in this section are set to 13 and 15 respectively. If the length of a section is d, the lower and upper limit of the train running time in this section are set to 4 and 6 repectively.

   (3) For each station, the lower and upper limit of the train dwell time are set to 1 and 2 respectively.

   (4) The departure time horizons of the last train on the up direction of line 1 at the departure station is [23:10, 23:15]. The departure time horizons of the last train on the down direction of line 1 at the departure station is [23:05, 23:10]. The departure time horizons of the last train on the up direction of line 2 at the departure station is [23:00, 23:05]. The departure time horizons of the last train on the down direction of line 2 at the departure station is [23:05, 23:10]. The departure time horizons of the last train on the up direction of line 3 at the departure station is [23:15, 23:20]. The departure time horizons of the last train on the down direction of line 3 at the departure station is [23:10, 23:15].

   (5) The transfer walking time at each transfer station is set to 1.5 min.
