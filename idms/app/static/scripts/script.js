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

  $('.dropdown-item:contains("Rename")').on("click", function () {
    var currentFilePath = $(this).closest(".file-item").data("absolute-path");
    var currentFileName = $(this).closest(".file-item").find(".file-item-name").text().trim();
    $("#currentFilePath").val(currentFilePath);
    $("#newFileName").val(currentFileName);
    $("#renameModal").modal("show");
  });

  $('.dropdown-item:contains("Move")').on("click", function () {
    var currentFilePath = $(this).closest(".file-item").find(".file-item-name").attr("href");
    var absoluteFilePath = $(this).closest(".file-item").data("absolute-path");

    $("#moveCurrentFilePath").val(currentFilePath);
    $("#moveAbsoluteFilePath").val(absoluteFilePath);
    $("#moveModal").modal("show");
  });

  $('.dropdown-menu a[href="javascript:void(0)"]:contains("Remove")').on("click", function () {
    var fileItem = $(this).closest(".file-item");
    var absolutePath = fileItem.data("absolute-path");

    // Set data attribute to modal delete button for reference
    $("#confirmDeleteBtn").data("absolute-path", absolutePath);
    $("#confirmDeleteModal").modal("show");
  });

  $("#confirmDeleteBtn").on("click", function () {
    var absolutePath = $(this).data("absolute-path");

    $.ajax({
      url: "/delete/",
      method: "POST",
      data: { absoluteFilePath: absolutePath },
      success: function (response) {
        // Handle success response if needed
        // For example, remove the file item from the UI
        $('[data-absolute-path="' + absolutePath + '"]').remove();
        $("#confirmDeleteModal").modal("hide");
      },
      error: function (xhr, status, error) {
        console.error("Error deleting file:", error);
        $("#confirmDeleteModal").modal("hide");
      },
    });
  });
});
