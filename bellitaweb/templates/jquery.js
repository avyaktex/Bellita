<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
          <script>
            $(document).ready(function() {
              $("form").submit(function(event) {
                event.preventDefault();
                var name = $("#input_name").val();
                var mob_num = $("#mobile_number").val();
                var date = $("#date").val();
                var time = $("#time").val();
                // Store the form data in local storage
                localStorage.setItem('input_name', name);
                localStorage.setItem('mobile_number',mob_num);
                localStorage.setItem('date',date);
                localStorage.setItem('time',time);
                // Redirect to the target HTML page
                window.location.href = "success.html";
              });
            });
          </script>


          <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script>
<script>
  $(document).ready(function() {
    // Retrieve the form data from local storage
    var name = localStorage.getItem('input_name');
    var mob_num = localStorage.getItem('mobile_number');
    var date = localStorage.getItem('date');
    var time = localStorage.getItem('time');
    // Display the retrieved data on the page
    $('#name').text(name);
    $('#mobile_number').text(mob_num);
    $('#date').text(date);
    $('#time').text(time);
    // Clear the stored form data from local storage
    localStorage.removeItem('name');
    localStorage.removeItem('mob_num');
    localStorage.removeItem('date');
    localStorage.removeItem('time');
  });
</script>