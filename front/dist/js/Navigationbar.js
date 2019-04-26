function FrontBase2() {
    var self = this;
}

FrontBase2.prototype.LiaddClass = function(){
  var li = $("#search");
  li.addClass('active').siblings().removeClass('active');
};

FrontBase2.prototype.run = function(){
  var self = this;
  self.LiaddClass();
};


$(function () {
   var f = new FrontBase2();
    f.run();
});