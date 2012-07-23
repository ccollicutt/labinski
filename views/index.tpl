%include header
        <div class="span9">
          <table class="table table-striped table-bordered table-condensed">
            <thead>
              <tr>
                <th colspan="2">Classes</th>
              </tr>
              <tr>
                <th>Name</th>
                <th>Make Reservation</th>
              </tr>
            </thead>
            <tbody>
              %for c in classes:
              <tr>
                <td>{{c.name}}</td>
                <td>
                  <div class="btn-group">
                    <button class="btn  dropdown-toggle" data-toggle="dropdown">Reserve<span class="caret"></span></button>
                    <ul class="dropdown-menu">
                      %for i in c.images:
                      <li><a href="/reserve">{{i.name}}</a></li>
                      %end
                    </ul>
                  </div><!-- /btn-group -->
                </td>
              </tr>
              %end #for c in classes
            </tbody>
          </table>
          <table class="table table-striped table-bordered table-condensed">
            <thead>
              <tr>
                <th colspan="2">Reservations</th>
              </tr>
              <tr>
                <th>Class Name</th>
                <th>Image</th>
                <th>Reservation Length</th>
                <th>Start Time</th>
                <th>End Time</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Econ 402</td>
                <td>Matlab</td>
                <td>4 hours</td>
                <td>Fri Jan 4, 16:05PM</td>
                <td>Fri Jan 4, 20:05PM</td>
                <td>Not Running</td>
              </tr>
            </tbody>
          </table>
          </div><!--/row-->
        </div><!--/span-->
%include footer