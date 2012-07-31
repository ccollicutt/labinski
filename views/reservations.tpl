%include header name=name
%include sidebar is_admin=is_admin
        <div class="span9">
          % if reservations:
          <table class="table table-striped table-bordered table-condensed">
            <thead>
              <tr>
                <th colspan="2">Reservations</th>
              </tr>
              <tr>
                <th>ID</th>
                <th>Class</th>
                <th>Image</th>
                <th>Image Type</th>
                <th>Status</th>
                <th></th>

              </tr>
            </thead>
            <tbody>
              %for r in reservations:
              <tr>
                <td>{{r.id}}
                <td>{{r.classes.name}}</td>
                <td>{{r.images.name}}</td>
                <td>{{r.images.imagetypes.name}}</td>
                <td>TBD</td>
                <td>
                  <div class="btn-group">
                    <a class="btn dropdown-toggle" data-toggle="dropdown" href="#">
                      Action
                      <span class="caret"></span>
                    </a>
                    <ul class="dropdown-menu">

                        <li><a href="/delete/reservation/{{r.id}}">Delete</a></li>
                  </div>
                </td>

              %end # for r in reservations
            </tbody>
          </table>
          %else: 
            <div class="alert">
               You have no reservations 
            </div>
          %end #if classes
        
          </div><!--/row-->
        </div><!--/span-->
%include footer