%include header
%include sidebar
        <div class="span9">
          % if reservations:
          <table class="table table-striped table-bordered table-condensed">
            <thead>
              <tr>
                <th colspan="2">Connections</th>
              </tr>
              <tr>
                <th>Reservation</th>
                <th>Other</th>
              </tr>
            </thead>
            <tbody>
              %for r in reservations:
              <tr>
                <td>{{r.name}}</td>
                <td>...</td>
              <tr>
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