%include header    
    <div class="container" align="center">
       <form class="form-horizontal" action="/reserve" method="post" name="reserve_form">
        <fieldset>


        <div class="control-group" style="width: 30%">
          <div class="control-group">
            <label class="control-label" for="image">Image Type</label>
            <div class="controls">
              <select id="image" name="image">
                <option value="matlab">matlab</option>
                <option value="hadoop">hadoop</option>
              </select>
            </div>
          </div>
          <div class="control-group">
            <label class="control-label" for="time_span">Time Span (hour)</label>
            <div class="controls">
              <select id="time_span" name="time_span">
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
              </select>
            </div>
          </div>  
        </div>
 
          <div class="form-actions">
            <button type="submit" class="btn btn-primary" data-toggle="button">Reserve</button>
            <button type="button" class="btn" onclick="logout()">Logout</button>
          </div>

        </fieldset>
    </form>
%include footer