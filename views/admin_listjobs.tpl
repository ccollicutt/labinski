%include header name=name
%include sidebar is_admin=is_admin
        <div class="span9">
          %if jobs:
          <table class="table table-striped table-bordered table-condensed">
            <thead>
              <tr>
                <th colspan="2">Scheduled Jobs</th>
              </tr>
              <tr>
                <th>ETA</th>
                <th>Name</th>
                <th>ID</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              %for job in jobs:
              <tr>
                <td>{{job.eta}}
                <td>{{job.name}}</td>
                <td>{{job.id}}</td>
                <td>{{job.status}}
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