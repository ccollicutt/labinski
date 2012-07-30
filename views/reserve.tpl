%include header name=name  
%include sidebar  
        <div class="span4">
        %if classes:
        <form class="form-horizontal" action="/reservation" method="post">
        <fieldset>
          <div class="control-group">
            <label class="control-label" for="select01">Start Time</label>
            <div class="controls">
              <select id="select01" name="start_time">
                    <option value="now">Now</option>
                    %for i in range(24):
                    <option value="{{i}}">{{i}}:00</option>
                    %end
              </select>
            </div>
          </div>
          <div class="control-group">
            <label class="control-label" for="select01">Class</label>
            <div class="controls">
              <select id="select02" name="class_name">
                    <option>Select Class</option>
                  % for c in classes:
                    <option value='{{c.name}}'>{{c.name}}</option>
                  %end # for c in classes
              </select>
            </div> <!-- class -->
          </div>
          <div class="control-group"</div>
            <label class="control-label" for="select01">Image</label>
            <div class="controls">
              <select id="select03" name="image_os_image_id">
                  <option>Select Image</option>
              </select>
            </div> <!-- image -->
          </div> <!-- control group -->

          <div class="control-group">
            <label class="control-label" for="reservation_length">Length</label>
            <div class="controls">
              <select id="select04" name="reservation_length">
                    <option value='1'>1 Hour</option>
                    <option value='2'>2 Hours</option>
                    <option value='4'>4 Hours</option>
                    <option value='8'>8 Hours</option>
              </select>
            </div>
          </div>

          <div class="form-actions">
            <button type="submit" class="btn btn-primary">Reserve</button>
            <!--<button class="btn">Cancel</button>-->
            <a class="btn" id="btn-next" href="/">Cancel</a>
          </div>
        </fieldset>
      </form>
      %else: 
      <div class="alert">
         You are not registered in any classes 
      </div>
      %end #if classes

          </div><!--/row-->
        </div><!--/span-->

<script type="text/javascript">
   $(document).ready(function(){
        $('#select02').bind('change', function(){

            $('#select03 option').remove();

            switch($(this).val()) {
            %for c in classes:
            case '{{c.name}}':
                % for i in c.images:
                $('#select03').append('<option value="{{i.os_image_id}}">{{i.name}}</option>');
                % end # for i in c.images
                break;
            %end # for c in classes

            }
        })
    });
</script>

%include footer