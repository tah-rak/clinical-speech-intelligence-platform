import PageHeader from '../components/layout/PageHeader';
import UploadForm from '../components/upload/UploadForm';

export default function UploadVisit() {
  return (
    <div>
      <PageHeader
        title="Upload Visit"
        subtitle="Upload clinical audio or use a sample transcript to demo the pipeline"
      />
      <UploadForm />
    </div>
  );
}
