(function ( $ ) {

  $.fn.celebrate = function(options){
      var end_size;
      var scale;
      var particle;
      var settings = $.extend({
                particles: 7,
                radius: 75,
                color: "black",
                unicode: '\u2605',
                start_size: '15',
                min_end_size: '20',
                max_end_size: '75',
                max_duration: 500,
                min_duration: 400,
                complete: function() {}
            },options);
    return this.each(function() {
      for(i=0;i<settings.particles;i++){
				scale = Math.random();
        end_size = (scale * (settings.max_end_size - settings.min_end_size) + settings.min_end_size);
        particle = $("<div>"+ settings.unicode +"</div>").addClass("particle");
        $(particle).css("position","absolute");
        $(particle).css("font-size", settings.start_size + "px");
        $(particle).css("opacity", 1);
        $(particle).css("z-index", 9999);
        $(particle).css("color", settings.color);
        $(particle).css("transform",'rotate(' + (Math.random() * 70) + 'deg)');
        $(this).append($(particle));
        $(particle).offset({
          top: $(this).offset().top + ($(this).height() / 2),
          left: $(this).offset().left + ($(this).width() / 2)
        });
        $(particle).animate(
          {
            "left": $(particle).offset().left + ((Math.random() < 0.5 ? -1 : 1) * (Math.random() * settings.radius)) +"px",
						"top": $(particle).offset().top + ((Math.random() < 0.5 ? -1 : 1) * (Math.random() * settings.radius)) +"px",
            "opacity":0.5,
            "z-index": 9999,
            "font-size": end_size +"px"
          },
					{
						"duration": (Math.random() * (settings.max_duration - settings.min_duration) + settings.min_duration),
						"complete": function (){
							$(this).animate({
                "opacity": 0
              },{
                "duration": settings.duration * 0.5,
                "complete": function(){
                  $(this).remove();
                }
              });
						}
					}
				);
      }
      settings.complete.call(this);
    });
  };
}( jQuery ));
