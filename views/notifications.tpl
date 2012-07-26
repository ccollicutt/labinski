%include header
%include sidebar
        <div class="span9">
          %if notifications:
          <table class="table table-striped table-bordered table-condensed">
            <thead>
              <tr>
                <th colspan="2">Notifications</th>
              </tr>
              <tr>
                <th>Status</th>
                <th>Message</th>
                <th>Time</th>
              </tr>
            </thead>
            <tbody>
              %for notification in notifications:
              <tr>
                <td>{{notification.status}}</td>
                <td>{{notification.message}}</td>
                <td>{{notification.time}}</td>
              <tr>
              %end #for notification in notifications
            </tbody>
          </table>
          %else: 
          <div class="alert">
             You have no notifications
         </div>
          %end #if notifications
        
          </div><!--/row-->
        </div><!--/span-->
%include footer