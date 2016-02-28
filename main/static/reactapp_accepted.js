/**
 * @jsx React.DOM
 */

window.Home = React.createClass({
  loadBidsFromServer: function() {
    $.ajax({
      url: this.props.get_url,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({data: JSON.parse(data)});
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.url, status, err.toString());
      }.bind(this)
    });
  },
  componentDidMount: function() {
    this.loadBidsFromServer();
    setInterval(this.loadBidsFromServer, this.props.pollInterval);
  },
	getInitialState: function() {
    	return {data: []};
  	},

  	deliverOrder: function(row){
  		debugger;
	    $.ajax({
	      url: this.props.uber_url,
	      dataType: 'json',
	      method: 'POST',
	      cache: false,
	      data: this.props.locationData,
	      success: function(data) {
	        debugger;
	      }.bind(this),
	      error: function(xhr, status, err) {
	        console.error(this.props.url, status, err.toString());
	      }.bind(this)
    	});  	
    },

	render: function() {
		var self = this;
		var orderNodes = this.state.data.map(function(row) {
		  var keywords = row.order.keywords.tags.map(function(tag){return "#" + tag.string})	      
		  var curBidPrice = ((row.min_bid.price)/100.0).toFixed(2);
		  var newBidPrice = ((row.min_bid.price - 50)/100.0).toFixed(2);
		  
		  var alreadyWinning = row.min_bid.item && (row.min_bid.item.restaurant === self.props.restaurant_id);
		  return (
			<div key={row.order.id} className={"order-row alert text-center row " + "alert-info"} role="alert">
	        <div className="order-col col-md-2 time-since">
	          {moment(row.order.bidding_end_time).fromNow()}
	        </div>
	        <div className="order-col info-area col-md-7">
	          <h3>Order for <i>"{row.item.name}"</i> (0.8 miles away) </h3>
	          <p><b>Keywords ordered:</b> {keywords.join(", ")}</p>
	          <p><i>{row.order.description}</i></p>
	        </div>
	        <div className="order-col col-md-3 uberstuff">
	          <a href="#" onClick={self.deliverOrder.bind(self, row)}>
	          <button className={"bid btn btn-default"}>
	          	<img height="50px" src="/static/uber.png"/>
	          	<span>Food ready? Deliver with Uber.</span>
	          </button>
	          </a>
	        </div>
	      </div>
	      );
	    });
		return (
			<div>
				{orderNodes}				
			</div>		
	    );
	},
});
