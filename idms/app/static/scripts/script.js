$(document).ready(function () {
  var selectedView = localStorage.getItem("file-manager-view") || "file-manager-col-view";
  var container = $(".file-manager-container");
  container.removeClass("file-manager-col-view file-manager-row-view").addClass(selectedView);
  $('input[name="file-manager-view"][value="' + selectedView + '"]').prop("checked", true);

  $('input[name="file-manager-view"]').on("change", function () {
    var selectedView = $(this).val();
    localStorage.setItem("file-manager-view", selectedView);
    container.removeClass("file-manager-col-view file-manager-row-view").addClass(selectedView);
    $(".file-item-tags-wrapper").toggleClass("file-manager-row-view", selectedView === "file-manager-row-view");
  });
});
