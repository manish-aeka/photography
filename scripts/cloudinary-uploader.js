/**
 * Cloudinary Image Uploader
 * Simple and direct upload to Cloudinary with progress tracking
 */

class CloudinaryUploader {
    constructor(config) {
        this.cloudName = config.cloudName || 'YOUR_CLOUD_NAME';
        this.uploadPreset = config.uploadPreset || 'YOUR_UNSIGNED_PRESET';
        this.folder = config.folder || 'photography-portfolio';
        this.uploadUrl = `https://api.cloudinary.com/v1_1/${this.cloudName}/image/upload`;
    }

    /**
     * Upload image to Cloudinary with progress tracking
     * @param {File} file - File to upload
     * @param {Function} onProgress - Progress callback (percentage)
     * @param {Object} options - Additional upload options (including maxSizeMB)
     * @returns {Promise<Object>} - Upload result
     */
    async upload(file, onProgress = null, options = {}) {
        // Validate file first
        const maxSizeMB = options.maxSizeMB || 10;
        const validation = this.validateFile(file, maxSizeMB);
        if (!validation.valid) {
            return {
                success: false,
                error: validation.error
            };
        }

        console.log('🚀 Starting Cloudinary upload...');
        console.log('📁 File:', file.name, `(${(file.size / (1024 * 1024)).toFixed(2)} MB)`);
        console.log('📏 Max Size:', maxSizeMB, 'MB');
        console.log('☁️ Cloud Name:', this.cloudName);
        console.log('🔑 Upload Preset:', this.uploadPreset);
        console.log('📂 Folder:', this.folder);
        console.log('🌐 Upload URL:', this.uploadUrl);

        return new Promise((resolve, reject) => {
            const formData = new FormData();
            formData.append('file', file);
            formData.append('upload_preset', this.uploadPreset);

            // Add folder if specified
            if (this.folder) {
                formData.append('folder', this.folder);
            }

            // Add tags if provided
            if (options.tags && Array.isArray(options.tags)) {
                formData.append('tags', options.tags.join(','));
            }

            // Add custom public_id if provided
            if (options.publicId) {
                formData.append('public_id', options.publicId);
            }

            console.log('📋 FormData prepared:', {
                file: file.name,
                upload_preset: this.uploadPreset,
                folder: this.folder
            });

            // Create XMLHttpRequest for progress tracking
            const xhr = new XMLHttpRequest();

            // Track upload progress
            xhr.upload.addEventListener('progress', (e) => {
                if (e.lengthComputable && onProgress) {
                    const percentage = Math.round((e.loaded / e.total) * 100);
                    const loadedMB = (e.loaded / (1024 * 1024)).toFixed(2);
                    const totalMB = (e.total / (1024 * 1024)).toFixed(2);
                    console.log(`📊 Upload Progress: ${percentage}% (${loadedMB}/${totalMB} MB)`);
                    onProgress(percentage);
                }
            });

            // Handle successful upload
            xhr.addEventListener('load', () => {
                console.log('📥 Response received. Status:', xhr.status);

                if (xhr.status === 200) {
                    try {
                        const data = JSON.parse(xhr.responseText);
                        console.log('✅ Upload successful!', data);
                        resolve({
                            success: true,
                            url: data.secure_url,
                            publicId: data.public_id,
                            width: data.width,
                            height: data.height,
                            format: data.format,
                            size: data.bytes,
                            thumbnail: this.getThumbnailUrl(data.public_id, 300),
                            originalUrl: data.url,
                            assetId: data.asset_id,
                            createdAt: data.created_at
                        });
                    } catch (error) {
                        console.error('❌ Failed to parse response:', error);
                        reject(new Error('Failed to parse response'));
                    }
                } else {
                    console.error('❌ Upload failed. Status:', xhr.status);
                    console.error('Response:', xhr.responseText);
                    try {
                        const error = JSON.parse(xhr.responseText);
                        const errorMsg = error.error?.message || JSON.stringify(error);
                        console.error('Error details:', errorMsg);
                        reject(new Error(errorMsg));
                    } catch {
                        reject(new Error(`Upload failed with status ${xhr.status}. Response: ${xhr.responseText}`));
                    }
                }
            });

            // Handle errors
            xhr.addEventListener('error', () => {
                console.error('❌ Network error during upload');
                reject(new Error('Network error during upload. Check your internet connection and CORS settings.'));
            });

            xhr.addEventListener('abort', () => {
                console.error('❌ Upload was aborted');
                reject(new Error('Upload was aborted'));
            });

            // Send request
            console.log('📤 Sending request to:', this.uploadUrl);
            xhr.open('POST', this.uploadUrl, true);
            xhr.send(formData);
        });
    }

    /**
     * Upload multiple images with progress tracking
     * @param {FileList|Array} files - Files to upload
     * @param {Function} onProgress - Progress callback (current, total, percentage)
     * @returns {Promise<Array>} - Array of upload results
     */
    async uploadMultiple(files, onProgress = null) {
        const results = [];
        const total = files.length;

        for (let i = 0; i < total; i++) {
            try {
                const result = await this.upload(
                    files[i],
                    (percentage) => {
                        if (onProgress) {
                            const overallPercentage = Math.round(((i + (percentage / 100)) / total) * 100);
                            onProgress(i + 1, total, overallPercentage, percentage);
                        }
                    }
                );
                results.push(result);
            } catch (error) {
                results.push({
                    success: false,
                    error: error.message,
                    fileName: files[i].name
                });
            }
        }

        return results;
    }

    /**
     * Get thumbnail URL
     * @param {string} publicId - Cloudinary public_id
     * @param {number} width - Thumbnail width
     * @returns {string} - Thumbnail URL
     */
    getThumbnailUrl(publicId, width = 300) {
        return `https://res.cloudinary.com/${this.cloudName}/image/upload/w_${width},c_fill/${publicId}`;
    }

    /**
     * Get transformed image URL
     * @param {string} publicId - Cloudinary public_id
     * @param {Object} transformations - Transformation options
     * @returns {string} - Transformed URL
     */
    getTransformedUrl(publicId, transformations = {}) {
        const baseUrl = `https://res.cloudinary.com/${this.cloudName}/image/upload`;

        const transformParts = [];

        if (transformations.width) transformParts.push(`w_${transformations.width}`);
        if (transformations.height) transformParts.push(`h_${transformations.height}`);
        if (transformations.crop) transformParts.push(`c_${transformations.crop}`);
        if (transformations.quality) transformParts.push(`q_${transformations.quality}`);
        if (transformations.format) transformParts.push(`f_${transformations.format}`);

        const transformString = transformParts.length > 0 ? transformParts.join(',') + '/' : '';

        return `${baseUrl}/${transformString}${publicId}`;
    }

    /**
     * Validate file before upload
     * @param {File} file - File to validate
     * @param {number} maxSizeMB - Maximum file size in MB
     * @returns {Object} - Validation result
     */
    validateFile(file, maxSizeMB = 10) {
        const allowedFormats = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/gif'];

        if (!file) {
            return { valid: false, error: 'No file provided' };
        }

        if (!allowedFormats.includes(file.type)) {
            return { valid: false, error: 'File format not supported. Use JPEG, PNG, WebP or GIF' };
        }

        const maxSize = maxSizeMB * 1024 * 1024;
        if (file.size > maxSize) {
            return { valid: false, error: `File size exceeds ${maxSizeMB}MB limit` };
        }

        return { valid: true };
    }
}

// Initialize with your Cloudinary credentials
const cloudinaryUploader = new CloudinaryUploader({
    cloudName: 'ddyo9iiz9',      // Replace with your cloud name
    uploadPreset: 'anupam-photography', // Replace with your upload preset
    folder: 'photography'
});

// Make available globally for editor
window.cloudinaryUploader = cloudinaryUploader;
