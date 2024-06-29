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
        $('[data-absolute-path="' + absolutePath + '"]').remove();
        $("#confirmDeleteModal").modal("hide");
      },
      error: function (xhr, status, error) {
        console.error("Error deleting file:", error);
        $("#confirmDeleteModal").modal("hide");
      },
    });
  });

  $('.dropdown-menu a[href="javascript:void(0)"]:contains("Move")').on("click", function () {
    var currentFilePath = $(this).closest(".file-item").data("absolute-path");
    $("#moveAbsoluteFilePath").val(currentFilePath);
    $("#moveModal").modal("show");
  });

  $("#chooseDirectoryBtn").on("click", function () {
    fetch("/choose_directory/")
      .then((response) => response.json())
      .then((data) => {
        $("#destinationPath").val(data.chosen_directory);
      });
  });

  $("#moveForm").on("submit", function (event) {
    event.preventDefault();
    const absoluteFilePath = $("#moveAbsoluteFilePath").val();
    const destinationPath = $("#destinationPath").val();

    fetch("/move/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        absoluteFilePath: absoluteFilePath,
        destinationPath: destinationPath,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        $("#moveModal").modal("hide");
        $("#successMessage").text("File moved to: " + data.destination_path);
        $("#successModal").modal("show");
      });
  });

  $("#successModal").on("hidden.bs.modal", function () {
    location.reload();
  });
});
