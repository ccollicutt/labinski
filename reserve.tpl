%include header    
        <div class="span4">
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
                    %for c in classes:
                      %for i in c.images:
                    <option>{{i.name}}</option>
                      %end # for i in c.images
                    %end # for c in classes
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
          </div><!--/row-->
        </div><!--/span-->
%include footer