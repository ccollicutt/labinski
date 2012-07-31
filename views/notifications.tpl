<<<<<<< HEAD
%include header name=name
%include sidebar is_admin=is_admin
=======
%include header
%include sidebar
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823
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
              </tr>
            </thead>
            <tbody>
<<<<<<< HEAD
              %for notification in notifications[0:25]:
=======
              %for notification in notifications[1:25]:
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823
              <tr>
                <td>{{notification.status}}</td>
                <td>{{notification.message}}</td>
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