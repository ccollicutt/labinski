    <div class="container-fluid">
      <div class="row-fluid">
        <div class="span3">
          <div class="well sidebar-nav">
            <ul class="nav nav-list">
              <li class="nav-header">Actions</li>
              <li><a href="/">Dashboard</a></li>
              <li><a href="/reservations">Current reservations</a></li>
              <li><a href="/reserve">Make reservation</a></li>
              <li><a href="/connections">Show connections</a></li>
              <li><a href="/images">Show images</a></li>
              <li><a href="/notifications">Notifications</a></li>
              %if is_admin == True:
                <li class="nav-header">Admin</li>
                <li><a href="/admin/listjobs">Show jobs</a></li>
              %end


            </ul>
          </div><!--/.well -->
        </div><!--/span-->