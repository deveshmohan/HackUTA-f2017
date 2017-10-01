<!DOCTYPE html>
<html>

<head>
  <title>Generic - Phantom by HTML5 UP</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <!--[if lte IE 8]><script src="assets/js/ie/html5shiv.js"></script><![endif]-->
  <link rel="stylesheet" href="assets/css/main.css">
  <!--[if lte IE 9]><link rel="stylesheet" href="assets/css/ie9.css" /><![endif]-->
  <!--[if lte IE 8]><link rel="stylesheet" href="assets/css/ie8.css" /><![endif]-->
</head>

<body>
  <!-- Wrapper -->
  <div id="wrapper">
    <!-- Header -->
    <header id="header">
      <div class="inner">
        <!-- Logo -->
        <a href="index.html" class="logo"> <span class="symbol"><img src="images/logo.svg" alt=""></span><span class="title">Shelterize</span> </a>
        <!-- Nav -->
        <nav>
          <ul>
            <li>
              <a href="#menu">Menu</a>
            </li>
          </ul>
        </nav>
      </div>
    </header>
    <!-- Menu -->
    <nav id="menu">
      <h2>Menu</h2>
      <ul>
        <li>
          <a href="index.html">Home</a>
        </li>
        <li>
          <a href="generic.html">Ipsum veroeros</a>
        </li>
        <li>
          <a href="generic.html">Tempus etiam</a>
        </li>
        <li>
          <a href="generic.html">Consequat dolor</a>
        </li>
        <li>
          <a href="elements.html">Elements</a>
        </li>
      </ul>
    </nav>
    <!-- Main -->
    <div id="main">
      <div class="inner">
        <h1>Help Me&nbsp;</h1> <span class="image main"><img src="images/pic13.jpg" alt=""></span>
        <form class="form-horizontal" role="form" method="POST" action="uploadhelpme.php">
          <div class="form-group"> <label>Name:</label>
            <input type="text" name="namein" class="form-control form-control-lg" placeholder="input name" id="subject" required="" data-validation-required-message="Please enter a subject"> </div>
          <div class="form-group"> <label>Address:</label>
            <input type="text" name="addressin" class="form-control form-control-lg" placeholder="input Address" id="subject" required="" data-validation-required-message="Please enter a subject"> </div>
          <div class="form-group"> <label>Phone #:</label>
            <input type="text" name="phonein" class="form-control form-control-lg" placeholder="input phone#" id="subject" required="" data-validation-required-message="Please enter a subject"> </div>
          <button type="submit" class="btn btn-primary">Submit</button>
        </form>
        


       <?php



//SQL DataBase log in information from the Cpanel in Godaddy

$servername = "localhost";
$username ="ironmountain";
$password ="jumpship";
$dbName ="riceshelter";


//create connection

$conn = new mysqli($servername, $username, $password, $dbName);

//check connection

if ($conn -> connect_error){
	die ("connection failed: " . $conn -> connect_error);
}


$sql = "SELECT * FROM `markers` ";

//If there is a connection display the results 
//It displays in a table format on the buttom 
//The echo commands display to the website

$result = $conn ->query($sql);

if ($result-> num_rows >0){

 echo '<div class="table-responsive">';
 echo '<table class="table table-striped">';

echo "<thead><tr>

<th>name</th>
<th>address #</th>
<th>Phone #</th>
<th>lat</th>
<th>long</th>


</tr>";

echo"</thead>";

	while($row = $result -> fetch_assoc()){

echo"<tbody>

<tr>

<td>" . $row["name"] . "</td>
<td>" . $row["address"] . "</td>
<td>" . $row["phone"] . "</td>
<td>" . $row["lat"] ."</td>
<td>" . $row["lng"] . "</td>
</tr>";

echo"</tbody>";

		}

        echo'</table>';
        echo'</div>';
       

}else{
	echo"0 results";
}

$conn->close();


?>












        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis dapibus rutrum facilisis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Etiam tristique libero eu nibh porttitor fermentum. Nullam venenatis
          erat id vehicula viverra. Nunc ultrices eros ut ultricies condimentum. Mauris risus lacus, blandit sit amet venenatis non, bibendum vitae dolor. Nunc lorem mauris, fringilla in aliquam at, euismod in lectus. Pellentesque habitant morbi tristique
          senectus et netus et malesuada fames ac turpis egestas. In non lorem sit amet elit placerat maximus. Pellentesque aliquam maximus risus, vel venenatis mauris vehicula hendrerit.</p>
      </div>
    </div>
    <!-- Footer -->
    <footer id="footer">
      <div class="inner">
        <section>
          <h2>Get in touch</h2>
          <form method="post" action="#">
            <div class="field half first">
              <input type="text" name="name" id="name" placeholder="Name"> </div>
            <div class="field half">
              <input type="email" name="email" id="email" placeholder="Email"> </div>
            <div class="field"> <textarea name="message" id="message" placeholder="Message"></textarea> </div>
            <ul class="actions">
              <li>
                <input type="submit" value="Send" class="special"> </li>
            </ul>
          </form>
        </section>
        <section>
          <h2>Follow</h2>
          <ul class="icons">
            <li>
              <a href="#" class="icon style2 fa-twitter"><span class="label">Twitter</span></a>
            </li>
            <li>
              <a href="#" class="icon style2 fa-facebook"><span class="label">Facebook</span></a>
            </li>
            <li>
              <a href="#" class="icon style2 fa-instagram"><span class="label">Instagram</span></a>
            </li>
            <li>
              <a href="#" class="icon style2 fa-dribbble"><span class="label">Dribbble</span></a>
            </li>
            <li>
              <a href="#" class="icon style2 fa-github"><span class="label">GitHub</span></a>
            </li>
            <li>
              <a href="#" class="icon style2 fa-500px"><span class="label">500px</span></a>
            </li>
            <li>
              <a href="#" class="icon style2 fa-phone"><span class="label">Phone</span></a>
            </li>
            <li>
              <a href="#" class="icon style2 fa-envelope-o"><span class="label">Email</span></a>
            </li>
          </ul>
        </section>
        <ul class="copyright">
          <li>© Untitled. All rights reserved</li>
          <li>Design:
            <a href="http://html5up.net">HTML5 UP</a>
          </li>
        </ul>
      </div>
    </footer>
  </div>
  <!-- Scripts -->
  <script src="assets/js/jquery.min.js"></script>
  <script src="assets/js/skel.min.js"></script>
  <script src="assets/js/util.js"></script>
  <!--[if lte IE 8]><script src="assets/js/ie/respond.min.js"></script><![endif]-->
  <script src="assets/js/main.js"></script>
</body>

</html>