<!DOCTYPE html>
<!--
To change this license header, choose License Headers in Project Properties.
Sarah Smith - Rewrote the dashboard populate

-->
<html>
    <head>
        <meta charset="UTF-8">
        <title></title>
    </head>
    <body>
        <?php

        function create_connection() {
            $link = mysqli_connect('localhost', 'fireworks', 'fireworks', 'fireworks');
            if (!$link) {
                printf("Connect failed: %s\n", mysqli_connect_error());
                exit();
            }
            return $link;
        }
		
        function dashboard_populate() {
			$connection = create_connection();
			
			$result1 = mysqli_query($connection, "CALL DashboardOutDay1;");
			if (!$result1) {
				die('Error executing query for Day 1: ' . mysqli_error($connection));
			}
			$row = mysqli_fetch_row($result1);
			$adultBandsNum1 = $row[0];
			$childBandsNum1 = $row[1];
			$genParkingNum1 = $row[2];
			$premiumParkingNum1 = $row[3];
			
			mysqli_next_result($connection);


			$result2 = mysqli_query($connection, "CALL DashboardOutDay2;");
			if (!$result2) {
				die('Error executing query for Day 2: ' . mysqli_error($connection));
			}
			$row = mysqli_fetch_row($result2);
			$adultBandsNum2 = $row[0];
			$childBandsNum2 = $row[1];
			$genParkingNum2 = $row[2];
			$premiumParkingNum2 = $row[3];
			mysqli_free_result($result2);

			mysqli_close($connection);

			return array(
				$adultBandsNum1, $childBandsNum1, $genParkingNum1, $premiumParkingNum1, 
				$adultBandsNum2, $childBandsNum2, $genParkingNum2, $premiumParkingNum2
			);
		}



        
        function user_login($connection) {
            $sql = 'SELECT * FROM company_cars WHERE make = ?';
            $stmt = mysqli_prepare($connection, $sql);
            $make = "GM";
            mysqli_stmt_bind_param($stmt, 's', $make);
            mysqli_stmt_execute($stmt);
            $result = mysqli_stmt_get_result($stmt);
            
            $row = mysqli_fetch_assoc($result);
            do {
                echo "</br><tr><td>{$row['LICENSE']} &nbsp;</td>";
                echo "<td>{$row['MODEL_YEAR']}&nbsp;</td>";
                echo "<td>{$row['MAKE']}&nbsp;</td>";
                echo "<td>{$row['MODEL']}&nbsp;</td>";
                echo "<td>{$row['MILEAGE']}&nbsp;</td>";
                echo "</tr>";
                $row = mysqli_fetch_assoc($result);
            } while ($row);
        }
        ?>
    </body>
</html>
