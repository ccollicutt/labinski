%include header  
%include sidebar  
        <div class="span4">
        %if images:
        <form class="form-horizontal" action="/reservation" method="post">
        <fieldset>
          <div class="control-group">
            <label class="control-label" for="select01">Start Time</label>
            <div class="controls">
              <select id="select01" name="reservation_time">
                    <option>Now</option>
                    %for i in range(24):
                    <option>{{i}}:00</option>
                    %end
              </select>
            </div>
          </div>
          <div class="control-group">
            <label class="control-label" for="select01">Image</label>
            <div class="controls">
              <select id="select01" name="reservation_image_name">
                      %for i in images:
                    <option>{{i.name}}</option>
                      %end # for i in images
              </select>
            </div>
          </div>
          <div class="control-group">
            <label class="control-label" for="reservation_length">Length</label>
            <div class="controls">
              <select id="select01" name="reservation_length">
                    <option>1 Hour</option>
                    <option>2 Hours</option>
                    <option>4 Hours</option>
                    <option>8 Hours</option>
              </select>
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn btn-primary">Reserve</button>
            <button class="btn">Cancel</button>
          </div>
        </fieldset>
      </form>
      %else: 
      <div class="alert">
         You are not registered in any classes 
      </div>
      %end #if images

          </div><!--/row-->
        </div><!--/span-->
%include footer