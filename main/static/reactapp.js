/**
 * @jsx React.DOM
 */

window.Home = React.createClass({
  loadBidsFromServer: function() {
    $.ajax({
      url: this.props.url,
      dataType: 'json',
      cache: false,
      success: function(data) {
        this.setState({data: data});
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
    	return {data: [{'order': {'name': "Cheese Pizza"}}]};
  	},
	render: function() {
		var orderNodes = this.state.data.map(function(row) {
	      return (
			<div className="order-row alert alert-info text-center row" role="alert">
	        <div className="order-col col-md-2">
	          <span className="time-left">55</span>
	          <span> Seconds left </span>
	        </div>
	        <div className="order-col info-area col-md-8">
	          <h4>Order for KEYWORDS HERE </h4>
	          Lalalalalala so much information here. List the keywords and distance away
	        </div>
	        <div className="order-col col-md-2">
	          <button className="bid btn">
	            Bid on Order for $8.50
	          </button>
	        </div>
	      </div>
	      );
	    });
		return (
			<div>
				{this.props.url}
				{orderNodes}				
			</div>		
	    );
	},
});
