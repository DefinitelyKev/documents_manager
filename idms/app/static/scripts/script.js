$(document).ready(function () {
	const selectedView = localStorage.getItem("file-manager-view") || "file-manager-col-view";
	const container = $(".file-manager-container");
	container.removeClass("file-manager-col-view file-manager-row-view").addClass(selectedView);
	$(`input[name="file-manager-view"][value="${selectedView}"]`).prop("checked", true);
	$(".container.flex-grow-1").show();

	$('input[name="file-manager-view"]').on("change", function () {
		const selectedView = $(this).val();
		localStorage.setItem("file-manager-view", selectedView);
		container.removeClass("file-manager-col-view file-manager-row-view").addClass(selectedView);
		$(".file-item-tags-wrapper").toggleClass("file-manager-row-view", selectedView === "file-manager-row-view");
	});

	$('.dropdown-item:contains("Rename")').on("click", function () {
		const currentFilePath = $(this).closest(".file-item").data("absolute-path");
		const currentFileName = $(this).closest(".file-item").find(".file-item-name").text().trim();
		$("#currentFilePath").val(currentFilePath);
		$("#newFileName").val(currentFileName);
		$("#renameModal").modal("show");
	});

	$('.dropdown-menu a[href="javascript:void(0)"]:contains("Remove")').on("click", function () {
		const fileItem = $(this).closest(".file-item");
		const absolutePath = fileItem.data("absolute-path");
		const fileName = fileItem.find(".file-item-name").text().trim();

		$("#confirmDeleteBtn").data("absolute-path", absolutePath);
		$("#filesToDeleteList").empty().append(`<li>${fileName}</li>`);
		$("#deleteMessage").text(`Are you sure you want to delete the following file?`);
		$("#confirmDeleteModal").modal("show");
	});

	$('.dropdown-menu a[href="javascript:void(0)"]:contains("No Sort")').on("click", function () {
		const fileItem = $(this).closest(".file-item");
		const absolutePath = fileItem.data("absolute-path");
		const fileName = fileItem.find(".file-item-name").text().trim();

		$("#confirmNoSortBtn").data("absolute-path", absolutePath);
		$("#filesToNoSortList").empty().append(`<li>${fileName}</li>`);
		$("#noSortMessage").text(`Are you sure you want to apply 'No Sort' to the following file?`);
		$("#confirmNoSortModal").modal("show");
	});

	$("#confirmDeleteBtn").on("click", function () {
		const absolutePath = $(this).data("absolute-path");
		if (absolutePath) {
			handleDelete([absolutePath]);
		} else {
			const selectedFiles = $(this).data("selected-files");
			if (selectedFiles && selectedFiles.length > 0) {
				handleDelete(selectedFiles);
			}
		}
	});

	$("#confirmNoSortBtn").on("click", function () {
		const absolutePath = $(this).data("absolute-path");
		if (absolutePath) {
			handleNoSort([absolutePath]);
		} else {
			const selectedFiles = $(this).data("selected-files");
			if (selectedFiles && selectedFiles.length > 0) {
				handleNoSort(selectedFiles);
			}
		}
	});

	$('.dropdown-menu a[href="javascript:void(0)"]:contains("Move")').on("click", function () {
		const currentFilePath = $(this).closest(".file-item").data("absolute-path");
		$("#moveAbsoluteFilePath").val(currentFilePath);
		$("#moveModal").modal("show");
	});

	$("#chooseDirectoryBtn").on("click", function () {
		fetch("/choose_directory/")
			.then(response => response.json())
			.then(data => {
				$("#destinationPath").val(data.chosen_directory);
			});
	});

	$("#moveForm").on("submit", function (event) {
		event.preventDefault();
		const absoluteFilePath = $("#moveAbsoluteFilePath").val();
		const destinationPath = $("#destinationPath").val();
		handleMove([absoluteFilePath], destinationPath);
	});

	$("#successModal").on("hidden.bs.modal", function () {
		location.reload();
	});

	$("#moveSelected").on("click", function () {
		const selectedFiles = getSelectedFiles();
		if (selectedFiles.length > 0) {
			$("#moveModal").modal("show");
			$("#moveForm")
				.off("submit")
				.on("submit", function (event) {
					event.preventDefault();
					const destinationPath = $("#destinationPath").val();
					handleMove(selectedFiles, destinationPath);
				});
		}
	});

	$("#removeSelected").on("click", function () {
		const { selectedFiles, fileNames } = getSelectedFilesAndNames();
		if (selectedFiles.length > 0) {
			$("#filesToDeleteList").empty();
			fileNames.forEach(name => $("#filesToDeleteList").append(`<li>${name}</li>`));
			$("#confirmDeleteModal").modal("show");
			$("#confirmDeleteBtn").data("selected-files", selectedFiles).data("absolute-path", null);
		}
	});

	$("#noSort").on("click", function () {
		const { selectedFiles, fileNames } = getSelectedFilesAndNames();
		if (selectedFiles.length > 0) {
			$("#filesToNoSortList").empty();
			fileNames.forEach(name => $("#filesToNoSortList").append(`<li>${name}</li>`));
			$("#confirmNoSortModal").modal("show");
			$("#confirmNoSortBtn").data("selected-files", selectedFiles).data("absolute-path", null);
		}
	});

	$(".file-item-checkbox input").on("change", function () {
		const filePath = $(this).closest(".file-item").data("absolute-path");
		const selectedFiles = $("#confirmDeleteBtn").data("selected-files") || [];
		if (this.checked) {
			selectedFiles.push(filePath);
		} else {
			const index = selectedFiles.indexOf(filePath);
			if (index > -1) {
				selectedFiles.splice(index, 1);
			}
		}
		$("#confirmDeleteBtn").data("selected-files", selectedFiles);

		// Update the file list in the modal
		const fileNames = selectedFiles.map(path => {
			return $(`[data-absolute-path="${path}"]`).find(".file-item-name").text().trim();
		});
		$("#filesToDeleteList").empty();
		fileNames.forEach(name => $("#filesToDeleteList").append(`<li>${name}</li>`));
	});

	const sortOptions = ["Name", "Tags", "Date Modified", "File Type", "Size"];
	function updateSortOptions() {
		const selectedOptions = $("#sortList select").map(function () { return $(this).val(); }).get();
		$("#sortList select").each(function () {
			const currentVal = $(this).val();
			$(this).empty().append('<option value="" disabled selected>Select a criterion</option>');
			sortOptions.forEach(option => {
				const optionValue = option.toLowerCase().replace(" ", "_");
				if (!selectedOptions.includes(optionValue) || optionValue === currentVal) {
					$(this).append(`<option value="${optionValue}">${option}</option>`);
				}
			});
			$(this).val(currentVal);
		});
		toggleAddSortButton();
		toggleFolderButtons();
	}

	function toggleAddSortButton() {
		const selectedOptionsCount = $("#sortList select").length;
		$("#addSortCriterion").prop("disabled", selectedOptionsCount >= sortOptions.length);
	}

	function toggleFolderButtons() {
		$("#sortList .list-group-item").each(function (index) {
			const folderButton = $(this).find(".folder-btn");
			if (index === 0 || $(this).prev().find(".folder-btn").is(":checked")) {
				folderButton.prop("disabled", false);
			} else {
				folderButton.prop("disabled", true);
				folderButton.prop("checked", false);
			}
		});
	}

	$("#addSortCriterion").on("click", function () {
		const sortList = $("#sortList");
		const sortItem = $('<li class="list-group-item d-flex justify-content-between align-items-center"></li>');
		const select = $('<select class="form-control mr-2" style="flex: 1 1 auto; width: auto;"><option value="" disabled selected>Select a criterion</option></select>');
		const removeButton = $('<button type="button" class="btn btn-danger btn-sm"><i class="bi bi-x-lg"></i></button>');
		const folderCheckbox = $('<label class="folder-checkbox ml-1 d-flex align-items-center"><div class="folder-btn-box"><input type="checkbox" class="folder-btn"><i class="bi bi-folder-plus"></i></div></label>');

		sortOptions.forEach(option => {
			select.append(`<option value="${option.toLowerCase().replace(" ", "_")}">${option}</option>`);
		});

		sortItem.append(select).append(folderCheckbox).append(removeButton);
		sortList.append(sortItem);

		updateSortOptions();

		sortList.sortable({ handle: '.sort-handle' });

		removeButton.on("click", function () {
			sortItem.remove();
			updateSortOptions();
		});

		select.on("change", function () {
			updateSortOptions();
		});

		folderCheckbox.find('input').on("change", function () {
			toggleFolderButtons();
		});
	});

	$("#saveSortOrder").on("click", function () {
		const sortOrder = $("#sortList select").map(function () { return $(this).val(); }).get();
		const folderCreation = $("#sortList .folder-btn").map(function () { return $(this).is(":checked"); }).get();

		$.ajax({
			url: "/sort/",
			method: "POST",
			contentType: "application/json",
			data: JSON.stringify({ sortOrder, folderCreation }),
			success: function (response) {
				console.log("Sort order saved successfully");
			},
			error: function (xhr, status, error) {
				console.error("Error saving sort order:", error);
			}
		});
		$("#sortModal").modal("hide");
	});

	function handleDelete(paths) {
		if (paths.length === 1) {
			$.ajax({
				url: "/delete/",
				method: "POST",
				data: { absoluteFilePath: paths[0] },
				success: function () {
					paths.forEach(path => $(`[data-absolute-path="${path}"]`).remove());
					$("#confirmDeleteModal").modal("hide");
				},
				error: function (xhr, status, error) {
					console.error("Error deleting file:", error);
					$("#confirmDeleteModal").modal("hide");
				}
			});
		} else {
			fetch("/delete_multiple/", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ absoluteFilePaths: paths })
			})
				.then(response => response.json())
				.then(() => {
					paths.forEach(path => $(`[data-absolute-path="${path}"]`).remove());
					$("#confirmDeleteModal").modal("hide");
				})
				.catch(error => {
					console.error("Error deleting files:", error);
					$("#confirmDeleteModal").modal("hide");
				});
		}
	}

	function handleNoSort(paths) {
		fetch("/no_sort/", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ absoluteFilePaths: paths })
		})
			.then(response => response.json())
			.then(() => {
				$("#confirmNoSortModal").modal("hide");
				$("#successMessage").text("No Sort applied to the selected files.");
				$("#successModal").modal("show");
			})
			.catch(error => {
				console.error("Error applying No Sort:", error);
				$("#confirmNoSortModal").modal("hide");
			});
	}

	function handleMove(paths, destinationPath) {
		fetch("/move/", {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ absoluteFilePath: paths[0], destinationPath: destinationPath })
		})
			.then(response => response.json())
			.then(data => {
				$("#moveModal").modal("hide");
				$("#successMessage").text("File moved to: " + data.destination_path);
				$("#successModal").modal("show");
			});
	}

	function getSelectedFiles() {
		return $(".file-item-checkbox input:checked").map(function () {
			return $(this).closest(".file-item").data("absolute-path");
		}).get();
	}

	function getSelectedFilesAndNames() {
		const selectedFiles = [];
		const fileNames = [];
		$(".file-item-checkbox input:checked").each(function () {
			const fileItem = $(this).closest(".file-item");
			selectedFiles.push(fileItem.data("absolute-path"));
			fileNames.push(fileItem.find(".file-item-name").text().trim());
		});
		return { selectedFiles, fileNames };
	}
});
