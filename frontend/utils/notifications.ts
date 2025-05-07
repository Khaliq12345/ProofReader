export function useNotifications() {
  const toast = useToast();
  const  showToast = (title : string, desc: string, icon: string, colorV: any)  => {
    toast.add({
      title: title,
      description: desc,
      icon: icon,
      color : colorV,
      closeIcon : 'i-heroicons-x-mark',
      close: {
        color: colorV,
        variant: 'outline',
        class: 'rounded-full'
      }
    })
  }
  return {
    showToast
  };
}