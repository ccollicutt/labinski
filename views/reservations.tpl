%include header
%include sidebar
        <div class="span9">
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
        
          </div><!--/row-->
        </div><!--/span-->
%include footer