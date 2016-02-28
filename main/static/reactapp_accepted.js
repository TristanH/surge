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

  		var sendData = $.extend({}, this.props.locationData);
  		sendData['order_id'] = row.order.id;
  		sendData['format'] = 'json'

		$.get(this.props.uber_url, 
			sendData,
			function(e){debugger;},
			 'json'
		);
    },

	render: function() {
		var self = this;
		var orderNodes = this.state.data.map(function(row) {
		  var keywords = row.order.keywords.tags.map(function(tag){return "#" + tag.string})	      
		  var curBidPrice = ((row.min_bid.price)/100.0).toFixed(2);
		  var newBidPrice = ((row.min_bid.price - 50)/100.0).toFixed(2);
		  
		  var alreadyWinning = !!row.order.pickup_time;
		  return (
			<div key={row.order.id} className={"order-row alert text-center row " + (alreadyWinning ? "alert-success" : "alert-info")} role="alert">
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
	          <button className={"bid btn btn-default" + (alreadyWinning ? " disabled" : "")}>
	          	<img height="50px" src="/static/uber.png"/>
	          	<span>{!alreadyWinning ? "Food ready? Deliver with Uber." : ("Your uber will arrive in " + moment(row.order.bidding_end_time).diff(moment.utc(), "seconds") + " seconds")}</span>
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
