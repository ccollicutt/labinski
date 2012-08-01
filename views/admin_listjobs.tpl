%include header name=name
%include sidebar is_admin=is_admin
        <div class="span9">
          %if jobs:
          <table class="table table-striped table-bordered table-condensed">
            <thead>
              <tr>
                <th colspan="2">Jobs</th>
              </tr>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Next Run Time</th>
              </tr>
            </thead>
            <tbody>
              %for job in jobs:
              <tr>
                <td>{{job.id}}</td>
                <td>{{job.name}}</td>
                <td>{{job.next_run_time}}</td>

              <tr>
              %end #for job in jobs
            </tbody>
          </table>
          %else: 
          <div class="alert">
             There are no jobs
         </div>
          %end #if jobs
        
          </div><!--/row-->
        </div><!--/span-->
%include footer