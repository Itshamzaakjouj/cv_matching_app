class CVUploadHandler {
    constructor() {
        this.dropZone = document.getElementById('dropZone');
        this.fileInput = document.getElementById('cvFiles');
        this.fileList = document.getElementById('fileList');
        this.uploadedFiles = new Set();
        
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // Gestion du drag & drop
        this.dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            this.dropZone.classList.add('border-blue-500', 'bg-blue-50');
        });

        this.dropZone.addEventListener('dragleave', () => {
            this.dropZone.classList.remove('border-blue-500', 'bg-blue-50');
        });

        this.dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            this.dropZone.classList.remove('border-blue-500', 'bg-blue-50');
            const files = e.dataTransfer.files;
            this.handleFiles(files);
        });

        // Gestion de la sélection de fichiers
        this.fileInput.addEventListener('change', (e) => {
            this.handleFiles(e.target.files);
        });
    }

    handleFiles(files) {
        Array.from(files).forEach(file => {
            if (this.isValidFile(file)) {
                this.addFile(file);
            } else {
                alert(`Le fichier "${file.name}" n'est pas un format accepté. Veuillez utiliser PDF, DOC ou DOCX.`);
            }
        });
    }

    isValidFile(file) {
        const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
        return validTypes.includes(file.type);
    }

    addFile(file) {
        if (this.uploadedFiles.has(file.name)) {
            alert(`Le fichier "${file.name}" a déjà été ajouté.`);
            return;
        }

        this.uploadedFiles.add(file.name);

        const fileElement = document.createElement('div');
        fileElement.className = 'bg-white rounded-lg p-4 shadow-sm border border-gray-200 hover:shadow-md transition-shadow';
        fileElement.innerHTML = `
            <div class="flex items-center justify-between">
                <div class="flex items-center space-x-3">
                    <div class="flex-shrink-0">
                        <i class="fas ${this.getFileIcon(file.type)} text-2xl ${this.getFileIconColor(file.type)}"></i>
                    </div>
                    <div class="flex-1 min-w-0">
                        <p class="text-sm font-medium text-gray-900 truncate filename">
                            ${file.name}
                        </p>
                        <p class="text-sm text-gray-500">
                            ${this.formatFileSize(file.size)}
                        </p>
                    </div>
                </div>
                <div class="flex items-center space-x-2">
                    <button onclick="window.cvUploadHandler.previewFile(this.parentElement.parentElement)" 
                            class="text-blue-600 hover:text-blue-800 transition-colors">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button onclick="window.cvUploadHandler.removeFile(this.parentElement.parentElement)" 
                            class="text-red-600 hover:text-red-800 transition-colors">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </div>
            </div>
            <div class="mt-2 h-1 bg-gray-200 rounded-full overflow-hidden">
                <div class="upload-progress h-1 bg-green-500 transition-all duration-300" style="width: 0%"></div>
            </div>
        `;

        this.fileList.appendChild(fileElement);

        // Simuler un téléchargement
        this.simulateUpload(fileElement);
    }

    simulateUpload(fileElement) {
        const progressBar = fileElement.querySelector('.upload-progress');
        let progress = 0;
        const interval = setInterval(() => {
            progress += 5;
            progressBar.style.width = `${progress}%`;
            if (progress >= 100) {
                clearInterval(interval);
                progressBar.parentElement.classList.add('hidden');
                fileElement.querySelector('.filename').classList.add('text-green-600');
                fileElement.querySelector('.filename').insertAdjacentHTML('beforeend', 
                    ' <i class="fas fa-check-circle text-green-500 ml-2"></i>');
            }
        }, 50);
    }

    removeFile(element) {
        const filename = element.querySelector('.filename').textContent.trim();
        this.uploadedFiles.delete(filename);
        element.classList.add('opacity-0');
        setTimeout(() => {
            element.remove();
            // Vérifier si la liste est vide
            if (this.fileList.children.length === 0) {
                this.fileList.innerHTML = `
                    <div class="text-center py-4 text-gray-500">
                        Aucun CV importé
                    </div>
                `;
            }
        }, 300);
    }

    previewFile(element) {
        const filename = element.querySelector('.filename').textContent.trim();
        // Ici, vous pouvez implémenter la prévisualisation du fichier
        alert(`Prévisualisation de ${filename}\nCette fonctionnalité sera bientôt disponible.`);
    }

    getFileIcon(type) {
        switch (type) {
            case 'application/pdf':
                return 'fa-file-pdf';
            case 'application/msword':
            case 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                return 'fa-file-word';
            default:
                return 'fa-file';
        }
    }

    getFileIconColor(type) {
        switch (type) {
            case 'application/pdf':
                return 'text-red-500';
            case 'application/msword':
            case 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                return 'text-blue-500';
            default:
                return 'text-gray-500';
        }
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    getUploadedFiles() {
        return Array.from(this.fileList.children).map(element => ({
            name: element.querySelector('.filename').textContent.trim(),
            element: element
        }));
    }
}

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', () => {
    window.cvUploadHandler = new CVUploadHandler();
});