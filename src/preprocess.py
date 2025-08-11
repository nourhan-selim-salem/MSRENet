# src/preprocess.py

import SimpleITK as sitk
import os

def denoise_image(image: sitk.Image) -> sitk.Image:
    """
    Reduces noise in an image using a denoising filter.
    This example uses the CurvatureFlowImageFilter.
    """
    denoiser = sitk.CurvatureFlowImageFilter()
    denoiser.SetNumberOfIterations(5)
    denoiser.SetTimeStep(0.05)
    return denoiser.Execute(image)

def register_to_flair(moving_image: sitk.Image, fixed_image: sitk.Image) -> sitk.Image:
    """
    Performs rigid registration of a moving image to a fixed image (FLAIR).
    """
    registration_method = sitk.ImageRegistrationMethod()

    # Set the metric, optimizer, and interpolator
    registration_method.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
    registration_method.SetOptimizerAsRegularStepGradientDescent(learningRate=1.0, minStep=1e-4, numberOfIterations=200)
    registration_method.SetInterpolator(sitk.sitkLinear)

    # Initialize the transform
    initial_transform = sitk.CenteredTransformInitializer(fixed_image,
                                                          moving_image,
                                                          sitk.Euler3DTransform(),
                                                          sitk.CenteredTransformInitializerFilter.GEOMETRY)
    registration_method.SetInitialTransform(initial_transform)

    final_transform = registration_method.Execute(sitk.Cast(fixed_image, sitk.sitkFloat32),
                                                  sitk.Cast(moving_image, sitk.sitkFloat32))

    # Resample the moving image to the fixed image space
    resampled_image = sitk.Resample(moving_image, fixed_image, final_transform, sitk.sitkLinear, 0.0, moving_image.GetPixelID())
    return resampled_image

def skull_strip(image: sitk.Image) -> sitk.Image:
    """
    Removes the skull from a brain MRI.
    This is a simplified example using thresholding and morphological operations.
    For robust skull stripping, a dedicated tool like FSL's BET, ANTs, or a deep learning model is recommended.
    """
    # A simple approach using Otsu thresholding
    otsu_filter = sitk.OtsuThresholdImageFilter()
    otsu_filter.SetInsideValue(0)
    otsu_filter.SetOutsideValue(1)
    brain_mask = otsu_filter.Execute(image)

    # Apply morphological closing to fill holes
    closing_filter = sitk.BinaryMorphologicalClosingImageFilter()
    closing_filter.SetKernelRadius(5)
    closed_mask = closing_filter.Execute(brain_mask)

    # Apply the mask to the original image
    mask_filter = sitk.MaskImageFilter()
    skull_stripped_image = mask_filter.Execute(image, closed_mask)
    return skull_stripped_image

def correct_bias_field(image: sitk.Image) -> sitk.Image:
    """
    Corrects for bias field inhomogeneities using the N4 algorithm. [2, 5]
    """
    # Create a mask to focus the correction on the brain tissue
    mask_image = sitk.OtsuThreshold(image, 0, 1, 200)

    # Cast the image to float32, as required by the N4 filter
    float_image = sitk.Cast(image, sitk.sitkFloat32)

    corrector = sitk.N4BiasFieldCorrectionImageFilter()
    corrected_image = corrector.Execute(float_image, mask_image)

    return sitk.Cast(corrected_image, image.GetPixelID())


def preprocess_pipeline(t1_path: str, t2_path: str, flair_path: str, output_dir: str):
    """
    Runs the full preprocessing pipeline for a single subject.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load images
    t1_image = sitk.ReadImage(t1_path)
    t2_image = sitk.ReadImage(t2_path)
    flair_image = sitk.ReadImage(flair_path)

    # --- Step 1: Denoising ---
    print("Step 1: Denoising images...")
    t1_denoised = denoise_image(t1_image)
    t2_denoised = denoise_image(t2_image)
    flair_denoised = denoise_image(flair_image)

    # --- Step 2: Rigid Registration ---
    print("Step 2: Registering T1 and T2 to FLAIR...")
    t1_registered = register_to_flair(t1_denoised, flair_denoised)
    t2_registered = register_to_flair(t2_denoised, flair_denoised)

    # --- Step 3: Skull Stripping ---
    print("Step 3: Skull stripping...")
    # Skull stripping is often best performed on the T1 image
    t1_skull_stripped = skull_strip(t1_registered)
    # The resulting mask can be applied to other modalities
    brain_mask = sitk.BinaryThreshold(t1_skull_stripped, lowerThreshold=1)
    flair_skull_stripped = sitk.Mask(flair_denoised, brain_mask)
    t2_skull_stripped = sitk.Mask(t2_registered, brain_mask)


    # --- Step 4: Bias Field Correction ---
    print("Step 4: Applying Bias Field Correction...")
    t1_final = correct_bias_field(t1_skull_stripped)
    t2_final = correct_bias_field(t2_skull_stripped)
    flair_final = correct_bias_field(flair_skull_stripped)

    # --- Save processed images ---
    print("Saving processed images...")
    sitk.WriteImage(t1_final, os.path.join(output_dir, "t1_processed.nii.gz"))
    sitk.WriteImage(t2_final, os.path.join(output_dir, "t2_processed.nii.gz"))
    sitk.WriteImage(flair_final, os.path.join(output_dir, "flair_processed.nii.gz"))

    print("Preprocessing complete.")



