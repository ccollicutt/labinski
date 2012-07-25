%include header 
%include sidebar
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
              %if classes:
                %for c in classes:
              <tr>
                <td>{{c.name}}</td>
                <td>
                  <div class="btn-group">
                    <button class="btn  dropdown-toggle" data-toggle="dropdown">Reserve<span class="caret"></span></button>
                    <ul class="dropdown-menu">
                      %for i in c.images:
                      <li><a href="/reserve/{{i.os_image_id}}/{{i.name}}">{{i.name}}</a></li>
                      %end
                    </ul>
                  </div><!-- /btn-group -->
                </td>
              </tr>
               %end #for c in classes
              %else:
                <tr>
                  <td colspan="2">No classes</td>
                </tr>
              %end # if classes
            </tbody>
          </table>

          </div><!--/row-->
        </div><!--/span-->
%include footer