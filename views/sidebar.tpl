    <div class="container-fluid">
      <div class="row-fluid">
        <div class="span3">
          <div class="well sidebar-nav">
            <ul class="nav nav-list">
              <li class="nav-header">Actions</li>
              <li><a href="/"><i class="icon-home"></i>Dashboard</a></li>
              <li><a href="/reservations"><i class="icon-book"></i>Current reservations</a></li>
              <li><a href="/reserve"><i class="icon-bookmark"></i>Make reservation</a></li>
              <li><a href="/connections"><i class="icon-eye-open"></i>Show connections</a></li>
              <li><a href="/images"><i class="icon-hdd"></i>Show images</a></li>
              <li><a href="/notifications"><i class="icon-envelope"></i>Notifications</a></li>
              %if is_admin == True:
                <li class="nav-header">Admin</li>
                <li><a href="/admin/listjobs"><i class="icon-list"></i>Show jobs</a></li>
              %end


            </ul>
          </div><!--/.well -->
        </div><!--/span-->