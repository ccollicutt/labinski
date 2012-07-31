<<<<<<< HEAD
%include header name=name
%include sidebar is_admin=is_admin
=======
%include header
%include sidebar
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823
        <div class="span9">
        %if images:
          <table class="table table-striped table-bordered table-condensed">
            <thead>
              <tr>
                <th colspan="2">Images</th>
              </tr>
              <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Services</th>
                <th>Description</th>
<<<<<<< HEAD
=======
                <th></th>
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823
              </tr>
            </thead>
            <tbody>
                %for i in images:
                <tr>
                  <td>{{i.name}}</td>
                  <td>{{i.imagetypes.name}}</td>
                  <td>
                    %for service in i.imagetypes.services:
                      {{service.name}}<br />
                    %end # for service in imagetypes.services
                  </td>

                  <td>{{i.description}}</td>
<<<<<<< HEAD
=======
                  <td><a class="btn" href="/reserve/{{i.os_image_id}}/{{i.name}}">Reserve</a></td>
>>>>>>> 67a385edefa25ba40bc5ec8682841d6bdcf6b823
                </tr>
                %end # for i in images
            </tbody>
          </table>
          %else: 
          <div class="alert">
             You are not registered in any classes 
          </div>
          %end #if images
        
          </div><!--/row-->
        </div><!--/span-->
%include footer