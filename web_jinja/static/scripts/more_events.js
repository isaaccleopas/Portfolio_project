<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script>
  $(document).ready(function() {
    var page = 1; // Initial page number
    var perPage = 9; // Number of events to fetch per page

    function loadMoreEvents() {
      $.ajax({
        url: '/more-events',
        method: 'GET',
        data: {
          page: page,
          perPage: perPage
        },
        success: function(response) {
          // Append the fetched events to the event list
          $('#event-list').append(response);

          // Increment the page number for the next request
          page++;

          // Hide the "Show More" button if no more events are available
          if (response.trim() === '') {
            $('#show-more-btn').hide();
          }
        },
        error: function(error) {
          console.log(error);
        }
      });
    }

    // Attach a click event handler to the "Show More" button
    $('#show-more-btn').click(function(e) {
      e.preventDefault();
      loadMoreEvents();
    });
  });
</script>
